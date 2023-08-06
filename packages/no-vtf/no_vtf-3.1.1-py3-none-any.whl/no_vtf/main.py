# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import contextlib
import functools
import inspect
import pathlib
import re
import sys

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, Union, cast, overload

import alive_progress
import click

import no_vtf

from no_vtf.filesystem import InputPaths, OutputDirectories
from no_vtf.image import ImageDataTypes, ImageDynamicRange
from no_vtf.pipeline import Pipeline
from no_vtf.task_runner import ParallelRunner, SequentialRunner, TaskRunner
from no_vtf.texture.decoder.vtf import VtfDecoder
from no_vtf.texture.extractor.vtf import VtfExtractor
from no_vtf.texture.filter import TextureCombinedFilter, TextureFilter
from no_vtf.texture.filter.vtf import (
    VtfFaceFilter,
    VtfFrameFilter,
    VtfMipmapFilter,
    VtfResolutionFilter,
    VtfSliceFilter,
)
from no_vtf.texture.namer.vtf import Vtf2TgaLikeNamer
from no_vtf.texture.vtf import VtfTexture

_T = TypeVar("_T")


def _show_credits(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return

    credits = """
    no_vtf - Valve Texture Format Converter
    Copyright (C) b5327157

    https://sr.ht/~b5327157/no_vtf/
    https://pypi.org/project/no-vtf/
    https://developer.valvesoftware.com/wiki/no_vtf

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with
    this program. If not, see <https://www.gnu.org/licenses/>.
    """

    click.echo(inspect.cleandoc(credits))
    ctx.exit()


class _Slice(click.ParamType):
    name = "slice"

    def get_metavar(self, param: click.Parameter) -> str:
        return "INDEX|[START]:[STOP][:STEP]"

    def convert(
        self,
        value: Union[str, slice],
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> slice:
        if isinstance(value, slice):
            return value

        slice_indices = self._to_slice_indices(value, param, ctx)

        start = slice_indices[0]
        if len(slice_indices) == 1:
            if start is None:
                self.fail("Index is empty.", param, ctx)
            if start >= 0:
                return slice(start, start + 1)
            else:
                stop = start + 1 if start != -1 else None
                return slice(start, stop)

        stop = slice_indices[1]
        if len(slice_indices) == 2:
            return slice(start, stop)

        step = slice_indices[2]
        if len(slice_indices) == 3:
            if step == 0:
                self.fail("Slice step cannot be zero.", param, ctx)
            return slice(start, stop, step)

        self.fail(f"Too many values in {value!r}.", param, ctx)

    def _to_slice_indices(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> list[Optional[int]]:
        slice_indices: list[Optional[int]] = []
        for slice_index in value.split(":"):
            if not slice_index:
                slice_indices.append(None)
            else:
                try:
                    slice_indices.append(int(slice_index))
                except ValueError:
                    self.fail(f"{slice_index!r} is not a valid integer.", param, ctx)
        return slice_indices


@click.command(name="no_vtf", no_args_is_help=True)
@click.argument(
    "paths",
    metavar="PATH...",
    type=click.Path(path_type=pathlib.Path, exists=True),
    required=True,
    nargs=-1,
)
@click.option(
    "--output-dir",
    "-o",
    "output_directory",
    help="Output directory",
    type=click.Path(path_type=pathlib.Path, exists=True, file_okay=False, dir_okay=True),
)
@click.option(
    "--output-file",
    help="Output file",
    type=click.Path(path_type=pathlib.Path, file_okay=True, dir_okay=False),
)
@click.option("--ldr-format", "-l", help="LDR output format  [default: tiff|apng]", type=str)
@click.option(
    "--hdr-format", "-h", help="HDR output format", show_default=True, type=str, default="exr"
)
@click.option(
    "--dynamic-range",
    "-d",
    help="Override LDR/HDR auto-detection",
    type=click.Choice(["ldr", "hdr"], case_sensitive=False),
)
@click.option(
    "--mipmaps",
    "-m",
    help="Extract all mipmaps",
    type=bool,
    is_flag=True,
)
@click.option(
    "--min-resolution",
    help="Minimum mipmap resolution",
    metavar="INTEGER",
    type=click.IntRange(min=1),
)
@click.option(
    "--max-resolution",
    help="Maximum mipmap resolution",
    metavar="INTEGER",
    type=click.IntRange(min=1),
)
@click.option(
    "--closest-resolution",
    help="Fallback to closest resolution if no exact match",
    type=bool,
    is_flag=True,
)
@click.option(
    "--frames",
    help="Frames to extract",
    type=_Slice(),
)
@click.option(
    "--faces",
    help="Faces to extract",
    type=_Slice(),
)
@click.option(
    "--slices",
    help="Slices to extract",
    type=_Slice(),
)
@click.option(
    "--animate",
    "-a",
    help="Output animated image file instead of writing each frame individually",
    type=bool,
    is_flag=True,
)
@click.option(
    "--fps",
    "-F",
    help="Frame rate used for animated image files",
    show_default=True,
    type=int,
    default=5,
)
@click.option(
    "--separate-channels",
    "-s",
    help="Output the RGB/L and A channels separately",
    type=bool,
    is_flag=True,
)
@click.option(
    "--overbright-factor",
    "-O",
    help="Multiplicative factor used for decoding compressed HDR textures",
    show_default=True,
    type=float,
    default=16.0,
)
@click.option(
    "--compress/--no-compress", help="Control lossless compression", type=bool, default=None
)
@click.option("write", "--always-write/--no-write", help="Write images", type=bool, default=None)
@click.option(
    "readback", "--readback/--no-readback", help="Readback images", type=bool, default=False
)
@click.option(
    "--num-workers",
    help="Number of workers for parallel conversion",
    metavar="INTEGER",
    type=click.IntRange(min=1),
)
@click.option(
    "--no-progress",
    help="Do not show the progress bar",
    type=bool,
    is_flag=True,
)
@click.version_option(version=no_vtf.__version__, message="%(version)s")
@click.option(
    "--credits",
    help="Show the credits and exit.",
    type=bool,
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=_show_credits,
)
def main_command(
    *,
    paths: Sequence[pathlib.Path],
    output_directory: Optional[pathlib.Path],
    output_file: Optional[pathlib.Path],
    ldr_format: Optional[str],
    hdr_format: str,
    dynamic_range: Optional[ImageDynamicRange],
    mipmaps: bool,
    min_resolution: Optional[int],
    max_resolution: Optional[int],
    closest_resolution: bool,
    frames: Optional[slice],
    faces: Optional[slice],
    slices: Optional[slice],
    animate: bool,
    fps: int,
    separate_channels: bool,
    overbright_factor: float,
    compress: Optional[bool],
    write: Optional[bool],
    readback: bool,
    num_workers: Optional[int],
    no_progress: bool,
) -> None:
    """
    Convert Valve Texture Format files into standard image files.

    PATH can be either file, or directory (in which case it is recursively searched
    for .vtf files, symbolic links are not followed). Multiple paths may be provided.

    As the output path, it is possible to specify either file or directory.

    Specifying the output file is useful mostly for single-file conversions,
    with filters to ensure only a single image will be written.

    If the output directory is not specified, images are output into the source directories.
    Otherwise, directory tree for any found files will be reconstructed in the chosen directory.

    Output LDR/HDR format is selected by its common file name extension.
    Special formats:
    "raw" to write the high resolution image data as-is;
    "skip" to skip the write step entirely.

    For supported formats, compression is controlled when saving the image.
    Lossless compression is enabled by default. Lossy compression is not used.

    The BGRA8888 format can store both LDR and compressed HDR images.
    The specific type is either auto-detected by looking at the input file name
    (roughly, if it contains "hdr" near the end), or can be set manually.

    It is possible to filter images to convert by min/max resolution (width & height),
    and by frames/faces/slices. The former supports exact or closest match. The latter
    supports selection by single index or via Python slicing:
    https://python-reference.readthedocs.io/en/latest/docs/brackets/slicing.html

    Face index mapping: right (0), left, back, front, up, down, sphere map (6).

    After applying filters, only the highest-resolution mipmap is converted by default.
    Alternatively, all mipmaps of the high-resolution image can be converted.

    Animated textures have frames converted into individual images by default.
    They can also be converted into an animated image file. When the latter
    is chosen, APNG is used as the default LDR image format instead of TIFF.

    The RGB/L and A channels are packed into one file by default.
    When output separately, resulting file names will be suffixed with "_rgb", "_l" or "_a".

    By default, image files are only written if they do not exist already.
    Alternatively, they can be overwritten, or writing can be disabled entirely.

    Images can be also read back to verify they have been written properly.
    Readback will error if data to be written do not match what is in the file.

    Worker is spawned for each logical core to run the conversion in parallel.
    Number of workers can be overridden. If set to 1, conversion is sequential.

    Exit status: Zero if all went successfully, non-zero if there was an error.
    Upon a recoverable error, conversion will proceed with the next file.
    """

    if output_file and output_directory:
        raise click.UsageError("Options --output-dir and --output-file are mutually exclusive")

    if output_file:
        main(
            paths=paths,
            output_file=output_file,
            ldr_format=ldr_format,
            hdr_format=hdr_format,
            dynamic_range=dynamic_range,
            mipmaps=mipmaps,
            min_resolution=min_resolution,
            max_resolution=max_resolution,
            closest_resolution=closest_resolution,
            frames=frames,
            faces=faces,
            slices=slices,
            animate=animate,
            fps=fps,
            separate_channels=separate_channels,
            overbright_factor=overbright_factor,
            compress=compress,
            write=write,
            readback=readback,
            num_workers=num_workers,
            no_progress=no_progress,
        )
    else:
        main(
            paths=paths,
            output_directory=output_directory,
            ldr_format=ldr_format,
            hdr_format=hdr_format,
            dynamic_range=dynamic_range,
            mipmaps=mipmaps,
            min_resolution=min_resolution,
            max_resolution=max_resolution,
            closest_resolution=closest_resolution,
            frames=frames,
            faces=faces,
            slices=slices,
            animate=animate,
            fps=fps,
            separate_channels=separate_channels,
            overbright_factor=overbright_factor,
            compress=compress,
            write=write,
            readback=readback,
            num_workers=num_workers,
            no_progress=no_progress,
        )


@overload
def main(
    *,
    paths: Sequence[pathlib.Path],
    output_directory: Optional[pathlib.Path],
    ldr_format: Optional[str] = None,
    hdr_format: Optional[str] = None,
    dynamic_range: Optional[ImageDynamicRange] = None,
    mipmaps: Optional[bool] = None,
    min_resolution: Optional[int] = None,
    max_resolution: Optional[int] = None,
    closest_resolution: Optional[bool] = None,
    frames: Optional[slice] = None,
    faces: Optional[slice] = None,
    slices: Optional[slice] = None,
    animate: Optional[bool] = None,
    fps: Optional[int] = None,
    separate_channels: Optional[bool] = None,
    overbright_factor: Optional[float] = None,
    compress: Optional[bool] = None,
    write: Optional[bool] = None,
    readback: Optional[bool] = None,
    num_workers: Optional[int] = None,
    no_progress: Optional[bool] = None,
) -> None:
    ...


@overload
def main(
    *,
    paths: Sequence[pathlib.Path],
    output_file: Optional[pathlib.Path],
    ldr_format: Optional[str] = None,
    hdr_format: Optional[str] = None,
    dynamic_range: Optional[ImageDynamicRange] = None,
    mipmaps: Optional[bool] = None,
    min_resolution: Optional[int] = None,
    max_resolution: Optional[int] = None,
    closest_resolution: Optional[bool] = None,
    frames: Optional[slice] = None,
    faces: Optional[slice] = None,
    slices: Optional[slice] = None,
    animate: Optional[bool] = None,
    fps: Optional[int] = None,
    separate_channels: Optional[bool] = None,
    overbright_factor: Optional[float] = None,
    compress: Optional[bool] = None,
    write: Optional[bool] = None,
    readback: Optional[bool] = None,
    num_workers: Optional[int] = None,
    no_progress: Optional[bool] = None,
) -> None:
    ...


def main(  # noqa: C901
    *,
    paths: Sequence[pathlib.Path],
    output_directory: Optional[pathlib.Path] = None,
    output_file: Optional[pathlib.Path] = None,
    ldr_format: Optional[str] = None,
    hdr_format: Optional[str] = None,
    dynamic_range: Optional[ImageDynamicRange] = None,
    mipmaps: Optional[bool] = None,
    min_resolution: Optional[int] = None,
    max_resolution: Optional[int] = None,
    closest_resolution: Optional[bool] = None,
    frames: Optional[slice] = None,
    faces: Optional[slice] = None,
    slices: Optional[slice] = None,
    animate: Optional[bool] = None,
    fps: Optional[int] = None,
    separate_channels: Optional[bool] = None,
    overbright_factor: Optional[float] = None,
    compress: Optional[bool] = None,
    write: Optional[bool] = None,
    readback: Optional[bool] = None,
    num_workers: Optional[int] = None,
    no_progress: Optional[bool] = None,
) -> None:
    params = main_command.params

    if hdr_format is None:
        hdr_format = _get_param_default(params, "hdr_format", str)
    if mipmaps is None:
        mipmaps = _get_param_default(params, "mipmaps", bool)
    if closest_resolution is None:
        closest_resolution = _get_param_default(params, "closest_resolution", bool)
    if animate is None:
        animate = _get_param_default(params, "animate", bool)
    if fps is None:
        fps = _get_param_default(params, "fps", int)
    if separate_channels is None:
        separate_channels = _get_param_default(params, "separate_channels", bool)
    if overbright_factor is None:
        overbright_factor = _get_param_default(params, "overbright_factor", float)
    if readback is None:
        readback = _get_param_default(params, "readback", bool)
    if no_progress is None:
        no_progress = _get_param_default(params, "no_progress", bool)

    if ldr_format is None:
        ldr_format = "tiff" if not animate else "apng"

    vtf_extension_pattern = re.compile(r"\.vtf$", re.ASCII | re.IGNORECASE)

    texture_filters = _get_filters(
        mipmaps=mipmaps,
        min_resolution=min_resolution,
        max_resolution=max_resolution,
        closest_resolution=closest_resolution,
        frames=frames,
        faces=faces,
        slices=slices,
    )

    texture_extractor = VtfExtractor()
    texture_filter = TextureCombinedFilter(texture_filters)
    texture_decoder = VtfDecoder(dynamic_range=dynamic_range, overbright_factor=overbright_factor)
    texture_namer = Vtf2TgaLikeNamer(include_mipmap_level=mipmaps, include_frame=(not animate))

    formats = [ldr_format, hdr_format]
    pipeline_initializer = functools.partial(Pipeline.initialize, formats)
    pipeline_initializer()

    pipeline = Pipeline(
        input_extension_pattern=vtf_extension_pattern,
        ldr_format=ldr_format,
        hdr_format=hdr_format,
        animate=animate,
        fps=fps,
        separate_channels=separate_channels,
        compress=compress,
        write=write,
        readback=readback,
        extractor=texture_extractor,
        filter=texture_filter,
        decoder=texture_decoder,
        namer=texture_namer,
    )

    input_paths = InputPaths(paths)
    if input_paths.has_directories():
        _resolve_directories(input_paths, not no_progress)

    task_runner: TaskRunner
    if num_workers is None or num_workers > 1:
        task_runner = ParallelRunner(max_workers=num_workers, initializer=pipeline_initializer)
    else:
        task_runner = SequentialRunner()

    if output_file:
        tasks = _get_tasks(pipeline, input_paths, output_file=output_file)
    else:
        tasks = _get_tasks(pipeline, input_paths, output_directory=output_directory)
    exit_status = _process_tasks(task_runner, tasks, not no_progress)
    sys.exit(exit_status)


def _get_param_default(
    params: Sequence[click.core.Parameter], param_name: str, param_type: type[_T]
) -> _T:
    for param in params:
        if param.name == param_name:
            default = param.default
            if callable(default):
                default = default()

            assert isinstance(default, param_type)
            return default

    raise RuntimeError(f"No such parameter: {param_name}")


def _get_filters(
    *,
    mipmaps: bool,
    min_resolution: Optional[int],
    max_resolution: Optional[int],
    closest_resolution: bool,
    frames: Optional[slice],
    faces: Optional[slice],
    slices: Optional[slice],
) -> Sequence[TextureFilter[VtfTexture]]:
    texture_filters: list[TextureFilter[VtfTexture]] = []

    if frames:
        texture_filters.append(VtfFrameFilter(frames=frames))
    if faces:
        texture_filters.append(VtfFaceFilter(faces=faces))
    if slices:
        texture_filters.append(VtfSliceFilter(slices=slices))
    if min_resolution is not None or max_resolution is not None:
        texture_filters.append(
            VtfResolutionFilter(
                min=min_resolution, max=max_resolution, closest_as_fallback=closest_resolution
            )
        )
    if not mipmaps:
        texture_filters.append(VtfMipmapFilter(mipmap_levels=slice(-1, None), last="filtered"))

    return texture_filters


def _resolve_directories(input_paths: InputPaths, show_progress: bool) -> None:
    progress_bar_manager = (
        alive_progress.alive_bar(receipt=False, spinner=None, theme="classic", enrich_print=False)
        if show_progress
        else None
    )
    with progress_bar_manager or contextlib.nullcontext() as progress_bar:
        for file in input_paths.search_in_directories("*.[vV][tT][fF]", add_results=True):
            if progress_bar:
                progress_bar.text = file.name
                progress_bar()
        input_paths.remove_directories()


def _get_tasks(
    pipeline: Pipeline[_T, ImageDataTypes],
    input_paths: InputPaths,
    *,
    output_directory: Optional[pathlib.Path] = None,
    output_file: Optional[pathlib.Path] = None,
) -> Sequence[_Task[_T]]:
    output_directories = OutputDirectories(output_directory)

    tasks: list[_Task[_T]] = []
    for input_file, input_base_directory in input_paths:
        if output_file:
            assert not output_directory, "output_file and output_directory are mutually exclusive"
            task = _Task(pipeline=pipeline, input_file=input_file, output_file=output_file)
        else:
            output_directory = output_directories(input_file, input_base_directory)
            task = _Task(
                pipeline=pipeline, input_file=input_file, output_directory=output_directory
            )
        tasks.append(task)
    return tasks


def _process_tasks(
    task_runner: TaskRunner,
    tasks: Sequence[_Task[_T]],
    show_progress: bool,
) -> int:
    exit_status = 0

    num_files = len(tasks)
    progress_bar_manager = (
        alive_progress.alive_bar(num_files, spinner=None, theme="classic", enrich_print=False)
        if show_progress
        else None
    )
    with progress_bar_manager or contextlib.nullcontext() as progress_bar:
        for task, result in task_runner(tasks):
            task = cast(_Task[_T], task)
            if isinstance(result, Pipeline.Receipt):
                if progress_bar:
                    skipped = not result.io_done
                    progress_bar(skipped=skipped)
                    progress_bar.text = str(task.input_file)
            else:
                exit_status = 1

                exception: Exception = result
                message = f"Error while processing {task!r}: {exception}"
                if exception.__cause__:
                    message += f" ({exception.__cause__})"
                click.echo(message, file=sys.stderr)

    return exit_status


@dataclass(frozen=True, kw_only=True)
class _Task(Generic[_T], TaskRunner.Task[Pipeline.Receipt]):
    pipeline: Pipeline[_T, ImageDataTypes]
    input_file: pathlib.Path
    output_directory: Optional[pathlib.Path] = None
    output_file: Optional[pathlib.Path] = None

    def __post__init(self) -> None:
        assert not (
            self.output_file and self.output_directory
        ), "output_file and output_directory are mutually exclusive"

    def __call__(self) -> Pipeline.Receipt:
        if self.output_file:
            return self.pipeline(self.input_file, output_file=self.output_file)
        else:
            assert self.output_directory, "either output_file or output_directory must be set"
            return self.pipeline(self.input_file, output_directory=self.output_directory)

    def __str__(self) -> str:
        return f"{self.input_file}"

    def __repr__(self) -> str:
        return f"{self.input_file!r}"
