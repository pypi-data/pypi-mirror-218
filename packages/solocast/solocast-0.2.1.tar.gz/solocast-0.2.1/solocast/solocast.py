#! /usr/bin/env python3

import os
import sys
from shutil import which

import click


RECORDING_DIRECTORY = "Recordings"
FORMAT = "wav"
script_segments = {}

MARKDOWN_HEADERS = (
    "# ",
    "## ",
    "### ",
    "#### ",
    "--- ",
)


def script_file_name():
    if os.path.exists("script.md"):
        return "script.md"
    return "script.txt"


def test_sox_exists():
    try:
        assert which("sox")
    except AssertionError:
        print("Cant find sox.  Install sox somewhere in your path.")
        sys.exit(1)


def get_recording_file_name(slug):
    return f"{RECORDING_DIRECTORY}/{slug}.{FORMAT}"


def project_prep():
    if not os.path.exists(RECORDING_DIRECTORY):
        os.makedirs(RECORDING_DIRECTORY)
    if not os.path.exists(f"{RECORDING_DIRECTORY}/Archive"):
        os.makedirs(f"{RECORDING_DIRECTORY}/Archive")


def wait_for_input():
    click.echo("*" * 40)
    _ = input("Press ENTER to Continue")


def add_slug_text(linetext):
    slug = linetext[:40].title()
    segment_name = "".join(filter(str.isalnum, slug))
    script_segments[segment_name] = linetext


def recording_exists(slug):
    if os.path.isfile(get_recording_file_name(slug)):
        return True
    return False


def script_exists():
    if os.path.isfile(script_file_name()):
        return True
    return False


def noise_profile_missing():
    if os.path.isfile(f"{RECORDING_DIRECTORY}/noise.prof"):
        return False
    return True


def combined_recording_exists():
    if os.path.isfile(f"{RECORDING_DIRECTORY}/combined.{FORMAT}"):
        return True
    return False


def truncate_audio(slug):
    recording = get_recording_file_name(slug)
    new_recording = f"{RECORDING_DIRECTORY}/{slug}-truncated.{FORMAT}"
    click.echo(f"truncating {recording}")

    SOX_CMD = (
        f"sox -V2 {recording}  {new_recording}   silence -l 1 0.1 .1% -1 1.0 .1%   stat"
    )
    click.echo(SOX_CMD)
    os.system(SOX_CMD)
    os.system(f" mv -v {recording} {RECORDING_DIRECTORY}/Archive/{slug}.{FORMAT}")
    os.rename(new_recording, recording)
    review_audio(slug)


def play_audio(slug):
    recording = get_recording_file_name(slug)
    click.echo(f"Playing {recording}")
    os.system(f"play {recording}")
    review_audio(slug)


def delete_audio(slug):
    recording = get_recording_file_name(slug)
    os.remove(recording)


def review_audio(slug):
    review_menu = ["(p)lay", "(a)ccept", "(r)eccord again", "(t)runcate"]
    click.echo(slug)
    for i in review_menu:
        click.echo(i)
    menu_action = input(">> ")
    if menu_action == "p":
        play_audio(slug)
    elif menu_action == "a":
        sys.exit()
    elif menu_action == "r":
        delete_audio(slug)
        find_and_record_next()
    elif menu_action == "t":
        truncate_audio(slug)
    else:
        review_audio(slug)


def record_audio(slug):
    new_recording = get_recording_file_name(slug)
    click.echo(f"Creating {new_recording}")
    click.echo("press Enter to start then CRTL-C to quit")
    wait_for_input()
    os.system(f"rec {new_recording}")


def record_silent_audio():
    silent_recording = f"{RECORDING_DIRECTORY}/silence.{FORMAT}"
    click.echo("solocast needs to record 5 seconds of silence")
    click.echo("Press Enter when you are ready")
    wait_for_input()
    os.system(f"rec {silent_recording} trim 0 5")
    os.system(f"sox {silent_recording} -n noiseprof {RECORDING_DIRECTORY}/noise.prof")


def load_txt():
    linetext = ""
    with open(script_file_name()) as script_file_reader:
        for line in script_file_reader.readlines():
            if not line.strip():
                add_slug_text(linetext)
                linetext = ""

            else:
                linetext += f"{line}  \n"
        add_slug_text(linetext)


def load_md():
    linetext = ""
    with open(script_file_name()) as script_file_reader:
        for line in script_file_reader.readlines():
            for markdown_header in MARKDOWN_HEADERS:
                if line.startswith(markdown_header) and linetext != "":
                    add_slug_text(linetext)
                    linetext = ""
            linetext += f"{line}  \n"
    add_slug_text(linetext)


def load_script():
    if script_file_name() == "script.md":
        load_md()
    else:
        load_txt()


def combine_recordings_for_export():
    recording_list = []
    combined_recording = f"{RECORDING_DIRECTORY}/combined.{FORMAT}"
    for slug, _text in script_segments.items():
        recording = get_recording_file_name(slug)
        recording_list.append(recording)
    recording_list_string = " ".join(recording_list)
    print(recording_list_string)
    SOX_CMD = f"sox  {recording_list_string}  {combined_recording} noisered {RECORDING_DIRECTORY}/noise.prof 0.21 norm -3"
    click.echo(SOX_CMD)
    os.system(SOX_CMD)


def export_to_flac():
    combined_recording = f"{RECORDING_DIRECTORY}/combined.{FORMAT}"
    flac_file = f"{RECORDING_DIRECTORY}/combined.flac"
    SOX_CMD = f"sox   {combined_recording} {flac_file}"
    click.echo(SOX_CMD)
    os.system(SOX_CMD)


def find_and_record_next():
    for slug, text in script_segments.items():
        if recording_exists(slug):
            continue
        click.clear()
        click.echo(slug)
        click.echo("*" * 40)
        click.echo(text)
        click.echo("*" * 40)
        record_audio(slug)
        review_audio(slug)


def complete_segment_count():
    recorded_count = 0
    for slug, _text in script_segments.items():
        if recording_exists(slug):
            recorded_count += 1
    return recorded_count


def print_status():
    segment_count = len(script_segments)
    complete = complete_segment_count()
    remaining = segment_count - complete
    if script_exists() is False:
        click.secho("No Script file", fg="red")
    else:
        click.echo("Segments:")
        click.echo(f"\t{segment_count} Total")
        click.echo(f"\t{complete_segment_count()} Complete")
        if remaining == 0:
            click.secho("All Segments Recorded", fg="green")
            if combined_recording_exists():
                click.secho("Combined Recording is Ready", fg="green")
            else:
                click.secho("No Combined Recording", fg="yellow")
        else:
            click.secho(f"\t{segment_count - complete} Remaining", fg="yellow")
    if noise_profile_missing():
        click.secho("No Noise Profile", fg="yellow")


@click.group()
def cli():
    test_sox_exists()
    if script_exists():
        load_script()


@cli.command()
def combine():
    "Combine Segments into single audio file"
    combine_recordings_for_export()


@cli.command()
def export():
    """Export combined recording to FLAC"""
    if not combined_recording_exists():
        combine_recordings_for_export()
    export_to_flac()


@cli.command()
def record():
    "Record next unrecorded segment"
    project_prep()
    if noise_profile_missing():
        record_silent_audio()
    find_and_record_next()


@cli.command()
def silence():
    "Generate noise profile"
    project_prep()
    record_silent_audio()


@cli.command()
def status():
    print_status()


# @cli.command()
# def print_recordings():
#    for slug, text in script_segments.items():
#        click.echo(slug, recording_exists(slug))


@cli.command()
def review():
    "Print segments"

    for slug, text in script_segments.items():
        click.clear()
        click.echo(slug)
        click.echo("*" * 40)
        click.echo()
        click.echo(text)
        wait_for_input()


if __name__ == "__main__":
    cli()
