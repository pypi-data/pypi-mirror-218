__ext_version__ = "1.2.1"

import os
import sys
import json
import shutil
import typer
import zipfile
import rich.progress
import requests as req
import subprocess as sp
from PIL import Image
from dotenv import load_dotenv
from appdirs import user_cache_dir

try:
    from .functions import error, generate_jwt
    from .classes import bcolors
except ImportError:
    from functions import error, generate_jwt
    from classes import bcolors

cached_app_build_dir = os.path.join(user_cache_dir("web-ext-helper", False), "build")
cached_app_data_env_dir = os.path.join(
    user_cache_dir("web-ext-helper", False), "data", ".env"
)
cached_app_dir = os.path.dirname(os.path.dirname(cached_app_build_dir))
os.makedirs(cached_app_build_dir, exist_ok=True)
os.makedirs(os.path.dirname(cached_app_data_env_dir), exist_ok=True)

web_ext_helper_logo = rf"""{bcolors.OKGREEN}
              ___.                              __            .__           .__                       
__  _  __ ____\_ |__             ____ ___  ____/  |_          |  |__   ____ |  | ______   ___________ 
\ \/ \/ // __ \| __ \   ______ _/ __ \\  \/  /\   __\  ______ |  |  \_/ __ \|  | \____ \_/ __ \_  __ \
 \     /\  ___/| \_\ \ /_____/ \  ___/ >    <  |  |   /_____/ |   Y  \  ___/|  |_|  |_> >  ___/|  | \/
  \/\_/  \___  >___  /          \___  >__/\_ \ |__|           |___|  /\___  >____/   __/ \___  >__|   
             \/    \/               \/      \/                     \/     \/     |__|        \/       

 Version: {bcolors.PURPLE}{__ext_version__}{bcolors.OKGREEN}
 An awesome CLI for {bcolors.OKCYAN}building{bcolors.OKGREEN}, {bcolors.OKCYAN}publishing {bcolors.OKGREEN}and {bcolors.OKCYAN}running {bcolors.PURPLE}web extensions.{bcolors.ENDC}"""

load_dotenv(cached_app_data_env_dir)

app = typer.Typer()

try:
    with open("src/manifest.json", "r") as manifest_file:
        manifest_data = json.load(manifest_file)

    manifest_name = manifest_data["name"]
    manifest_name_lower = manifest_data["name"].lower()
    manifest_version = manifest_data["version"]
except FileNotFoundError:
    manifest_name_lower = None
    manifest_version = None

if len(sys.argv) == 2 and sys.argv[1] == "-h":
    sys.argv[1] = "--help"

if len(sys.argv) == 2 and sys.argv[1] == "--help":
    typer.echo(web_ext_helper_logo)


@app.command(help="Show the version of the extension", name="version")
def __version__():
    typer.echo(
        f"{bcolors.OKGREEN}Current {bcolors.OKCYAN}web-ext-helper{bcolors.OKGREEN} version: {bcolors.PURPLE}{__ext_version__}{bcolors.ENDC}"
    )


@app.command(help="Build the extension from the files in the src folder", name="build")
def __build__(
    compress: bool = typer.Option(
        True, "--compress", "-co", help="Compress the output"
    ),
    clean: bool = typer.Option(False, "--clean", "-cl", help="Clean the build folder"),
):
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    if clean:
        shutil.rmtree(cached_app_build_dir)
        os.mkdir(cached_app_build_dir)

    name = f"{cached_app_build_dir}/{manifest_name_lower}-{manifest_version}.zip"

    with rich.progress.Progress(
        "[progress.description]{task.description}",
        "[progress.percentage]{task.percentage:>3.0f}%",
        rich.progress.BarColumn(),
        rich.progress.TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("[green]Building...", total=100)
        total_file_count = sum(len(files) for _, _, files in os.walk("src"))
        processed_file_count = 0

        with zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED) as build:
            for root, _, files in os.walk("src"):
                for file in files:
                    if file != "src":
                        description = f"Adding file: {bcolors.OKCYAN}{os.path.relpath(os.path.join(root, file), 'src')}{bcolors.ENDC} to output file"
                        build.write(
                            os.path.join(root, file),
                            os.path.relpath(os.path.join(root, file), "src"),
                            compress_type=zipfile.ZIP_DEFLATED if compress else None,
                        )

                        processed_file_count += 1
                        progress_percentage = (
                            processed_file_count / total_file_count
                        ) * 100
                        progress.update(
                            task,
                            advance=progress_percentage
                            - progress.tasks[task].completed,
                            description=description,
                        )

    typer.echo(
        f"\n{bcolors.OKGREEN}Extension built successfully in {bcolors.PURPLE}{progress.tasks[task].finished_time:.2f}{bcolors.OKGREEN} seconds.{bcolors.ENDC}"
    )


@app.command(help="Validate the extension", name="validate")
def __validate__():
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    typer.echo(f"{bcolors.OKCYAN}Validating extension...{bcolors.ENDC}")

    try:
        sp.run(
            [
                r"C:\Program Files\nodejs\web-ext.cmd",
                "lint",
                "--source-dir",
                "src",
            ],
        )
    except FileNotFoundError:
        error(
            "web-ext not found. Please install it globally using 'npm install -g web-ext'"
        )
        raise typer.Exit(1)
    except sp.CalledProcessError as e:
        typer.echo(f"{bcolors.FAIL}{e.stderr.decode()}{bcolors.ENDC}", err=True)
        raise typer.Exit(1)


@app.command(help="Run the extension in Firefox", name="run")
def __run__():
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    typer.echo(f"{bcolors.OKCYAN}Running extension...{bcolors.ENDC}")

    try:
        sp.run(
            [
                r"C:\Program Files\nodejs\web-ext.cmd",
                "run",
                "--source-dir",
                "src",
            ],
        )
    except FileNotFoundError:
        error(
            "web-ext not found. Please install it globally using 'npm install -g web-ext'"
        )
        raise typer.Exit(1)
    except sp.CalledProcessError as e:
        typer.echo(f"{bcolors.FAIL}{e.stderr.decode()}{bcolors.ENDC}", err=True)
        raise typer.Exit(1)


@app.command(help="Sign the extension for self-hosting the extension", name="sign")
def __sign__():
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    with rich.progress.Progress(
        "[progress.description]{task.description}",
        "[progress.percentage]{task.percentage:>3.0f}%",
        rich.progress.BarColumn(),
        rich.progress.TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("[green]Signing extension...", total=100)

        try:
            api_key, api_secret = os.environ.get("AMO_API_KEY", None), os.environ.get(
                "AMO_API_SECRET", None
            )

            if api_key is None or api_secret is None:
                error(
                    "AMO_API_KEY and AMO_API_SECRET environment variables not found.\nPlease set them using the set-amo-credentials command before publishing the extension"
                )
                raise typer.Exit(1)

            sp.run(
                [
                    r"C:\Program Files\nodejs\web-ext.cmd",
                    "sign",
                    "--channel=unlisted",
                    "--source-dir",
                    "src",
                    f"--api-key={api_key}",
                    f"--api-secret={api_secret}",
                ],
            )
            progress.update(task, advance=100, description="Signing extension...")
        except FileNotFoundError:
            error(
                "web-ext not found. Please install it globally using 'npm install -g web-ext'"
            )
            raise typer.Exit(1)
        except sp.CalledProcessError as e:
            typer.echo(f"{bcolors.FAIL}{e.stderr.decode()}{bcolors.ENDC}", err=True)
            raise typer.Exit(1)


@app.command(help="Publish the extension to the Mozilla Addons Store", name="publish")
def __publish__():
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    typer.echo(f"{bcolors.OKCYAN}Publishing extension...{bcolors.ENDC}")

    try:
        api_key, api_secret = os.environ.get("AMO_API_KEY", None), os.environ.get(
            "AMO_API_SECRET", None
        )

        if api_key is None or api_secret is None:
            error(
                "AMO_API_KEY and AMO_API_SECRET environment variables not found.\nPlease set them using the set-amo-credentials command before publishing the extension"
            )
            raise typer.Exit(1)

        sp.run(
            [
                r"C:\Program Files\nodejs\web-ext.cmd",
                "sign",
                "--channel=listed",
                "--source-dir",
                "src",
                f"--api-key={api_key}",
                f"--api-secret={api_secret}",
            ],
        )
    except FileNotFoundError:
        error(
            "web-ext not found. Please install it globally using 'npm install -g web-ext'"
        )
        raise typer.Exit(1)
    except sp.CalledProcessError as e:
        typer.echo(f"{bcolors.FAIL}{e.stderr.decode()}{bcolors.ENDC}", err=True)
        raise typer.Exit(1)


@app.command(help="Delete the extension from the Mozilla Addons Store", name="delete")
def __delete__(confirm: bool = typer.Option(False, "--confirm", "-c")):
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    if not confirm:
        typer.confirm(
            f"Are you sure you want to delete the extension from the Mozilla Addons Store?: {bcolors.OKCYAN}{manifest_name} v{manifest_version}{bcolors.ENDC}",
            abort=True,
        )

    typer.echo(f"{bcolors.OKCYAN}Deleting extension...{bcolors.ENDC}")

    try:
        with open("src/manifest.json", "r") as manifest_file:
            manifest_data = json.load(manifest_file)
            guid = manifest_data["browser_specific_settings"]["gecko"]["id"]

        api_key, api_secret = os.environ.get("AMO_API_KEY", None), os.environ.get(
            "AMO_API_SECRET", None
        )

        if api_key is None or api_secret is None:
            error(
                "AMO_API_KEY and AMO_API_SECRET environment variables not found.\nPlease set them using the set-amo-credentials command before deleting the extension"
            )
            raise typer.Exit(1)

        jwt_token = generate_jwt(api_key, api_secret)

        res = req.get(
            f"https://addons.mozilla.org/api/v5/addons/addon/{guid}/delete_confirm",
            headers={
                "Authorization": f"JWT {jwt_token}",
            },
        )
        delete_confirm_token = res.json()["delete_confirm"]

        req.delete(
            f"https://addons.mozilla.org/api/v5/addons/addon/{guid}",
            headers={
                "Authorization": f"JWT {jwt_token}",
            },
            params={
                "delete_confirm": delete_confirm_token,
            },
        )

        typer.echo(
            f"{bcolors.OKGREEN}Successfully deleted extension from the Mozilla Addons Store: {bcolors.OKCYAN}{manifest_name} with Addon ID {guid}{bcolors.ENDC}"
        )
    except req.exceptions.HTTPError as e:
        typer.echo(f"{bcolors.FAIL}{e.response.text}{bcolors.ENDC}", err=True)
        raise typer.Exit(1)


@app.command(
    help="Delete the credentials for the Mozilla Addons Store",
    name="del-amo-credentials",
)
def __del_amo_credentials__():
    if os.path.exists(cached_app_data_env_dir):
        os.remove(cached_app_data_env_dir)

    typer.echo(
        f"{bcolors.OKGREEN}Successfully deleted the credentials for the Mozilla Addons Store{bcolors.ENDC}"
    )


@app.command(
    help="Set the credentials for the Mozilla Addons Store", name="set-amo-credentials"
)
def __set_amo_credentials__(
    api_key: str = typer.Option(
        ...,
        "--api-key",
        "-k",
        help="The API key for the Mozilla Addons Store",
    ),
    api_secret: str = typer.Option(
        ...,
        "--api-secret",
        "-s",
        help="The API secret for the Mozilla Addons Store",
    ),
):
    with open(cached_app_data_env_dir, "w") as env_file:
        env_file.write(f"AMO_API_KEY={api_key}\n")
        env_file.write(f"AMO_API_SECRET={api_secret}\n")

    typer.echo(
        f"{bcolors.OKGREEN}Successfully set the credentials for the Mozilla Addons Store{bcolors.ENDC}"
    )


@app.command(
    help="Clean all files and folders created by web-ext-helper (including the build folder and the cache folder)",
    name="clean",
)
def __clean__():
    shutil.rmtree("__pycache__", ignore_errors=True)
    shutil.rmtree(cached_app_dir, ignore_errors=True)

    typer.echo(
        f"{bcolors.OKGREEN}All files and folders created by {bcolors.OKCYAN}web-ext-helper{bcolors.OKGREEN} have been deleted.{bcolors.ENDC}"
    )


@app.command(
    help="View the current manifest.json file of the extension", name="manifest"
)
def __manifest__():
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    with open("src/manifest.json", "r") as manifest_file:
        manifest_data = json.load(manifest_file)

    logo_data = manifest_data["browser_action"].get("default_icon", None)
    if logo_data is not None:
        logo_path = list(logo_data.values())[0]
        logo_size = list(logo_data.keys())[0]
    else:
        logo_path = None
        logo_size = None

    typer.echo(
        f"""
Name: {manifest_data["name"]}
Version: {manifest_data["version"]}
Description: {manifest_data["description"]}
Permissions: {manifest_data["permissions"]}
Logo: {logo_path}
Logo size: {logo_size} px
Browser action title: {manifest_data["browser_action"]["default_title"]}
Strict minimum version: {manifest_data["browser_specific_settings"]["gecko"]["strict_min_version"]}
App ID: {manifest_data["browser_specific_settings"]["gecko"]["id"]}
"""
    )


@app.command(help="Initialize a new extension", name="init")
def __init__():
    if os.path.exists("src/manifest.json"):
        error("src/manifest.json already exists")
        raise typer.Exit(1)

    def ask_for_input(
        is_validation,
        name,
        version,
        description,
        permissions,
        logo,
        browser_action_title,
        strict_min_version,
        app_id,
    ):
        name = typer.prompt(
            f"Name of the extension ({bcolors.FAIL}required{bcolors.ENDC})",
            default=f"{bcolors.OKGREEN}{name}{bcolors.ENDC}"
            if name is not None
            else None,
        )
        version = typer.prompt(
            "Version of the extension",
            default=f"{bcolors.OKGREEN}{version}{bcolors.ENDC}"
            if is_validation
            else f"{bcolors.OKGREEN}1.0.0{bcolors.ENDC}",
        )
        version = version.replace(bcolors.OKGREEN, "").replace(bcolors.ENDC, "")
        if len(version.split(".")) != 3:
            error("Version must follow the pattern major.minor.patch")
            raise typer.Exit(1)
        description = typer.prompt(
            f"Description of the extension ({bcolors.FAIL}required{bcolors.ENDC})",
            default=f"{bcolors.OKGREEN}{description}{bcolors.ENDC}"
            if description is not None
            else None,
        )
        permissions = typer.prompt(
            f"Permissions of the extension ({bcolors.PURPLE}separated by ','{bcolors.ENDC})",
            default=f"{bcolors.OKGREEN}{', '.join(permissions)}{bcolors.ENDC}"
            if is_validation
            else "",
        )
        permissions = (
            list(map(lambda x: x.strip(), permissions.split(",")))
            if permissions != ""
            else []
        )
        logo = typer.prompt(
            f"Path to logo of the extension ({bcolors.PURPLE}leave blank for none{bcolors.ENDC})",
            default=(
                f"{bcolors.OKGREEN}{logo}{bcolors.ENDC}" if logo is not None else ""
            )
            if is_validation
            else "",
            show_default=False if not is_validation else True,
        )
        if logo == "":
            logo = None
        else:
            if not os.path.exists(logo):
                error("Logo not found")
                raise typer.Exit(1)

            try:
                Image.open(logo)
            except:
                error("Invalid image")
                raise typer.Exit(1)
        browser_action_title = typer.prompt(
            "Title of the browser action",
            default=f"{bcolors.OKGREEN}{browser_action_title}{bcolors.ENDC}"
            if is_validation
            else f"{bcolors.OKGREEN}{name}{bcolors.ENDC}",
        )
        browser_action_title = browser_action_title.replace(
            bcolors.OKGREEN, ""
        ).replace(bcolors.ENDC, "")
        strict_min_version = typer.prompt(
            "Strict minimum version of Firefox",
            default=f"{bcolors.OKGREEN}{strict_min_version}{bcolors.ENDC}"
            if is_validation
            else f"{bcolors.OKGREEN}48.0{bcolors.ENDC}",
        )
        if strict_min_version == "\x1b[92m48.0\x1b[0m":
            strict_min_version = "48.0"
        assert float(strict_min_version) >= 48.0
        app_id = typer.prompt(
            f"App ID of the extension ({bcolors.FAIL}required{bcolors.ENDC})",
            default=f"{bcolors.OKGREEN}{app_id}{bcolors.ENDC}"
            if app_id is not None
            else None,
        )

        def validate_input():
            prompt = typer.prompt(
                f"""
Name: {bcolors.PURPLE}{name}{bcolors.ENDC}
Version: {bcolors.PURPLE}{version}{bcolors.ENDC}
Description: {bcolors.PURPLE}{description}{bcolors.ENDC}
Permissions: {bcolors.PURPLE}{permissions}{bcolors.ENDC}
Logo: {bcolors.PURPLE}{logo}{bcolors.ENDC}
Browser action title: {bcolors.PURPLE}{browser_action_title}{bcolors.ENDC}
Strict minimum version: {bcolors.PURPLE}{strict_min_version}{bcolors.ENDC}
App ID: {bcolors.PURPLE}{app_id}{bcolors.ENDC}

    """,
                prompt_suffix=f"{bcolors.OKCYAN}Continue? [Y/n]:{bcolors.ENDC}",
            ).lower()
            if prompt in ["n", "no"]:
                typer.echo("\n")
                return ask_for_input(
                    True,
                    name,
                    version,
                    description,
                    permissions,
                    logo,
                    browser_action_title,
                    strict_min_version,
                    app_id,
                )
            elif prompt not in ["y", "yes", ""]:
                return validate_input()

        validate_input()

        if name == "" or description == "" or app_id == "":
            error("Name, description and app ID are required")
            raise typer.Exit(1)

        if logo != None and not os.path.exists(logo):
            error("Logo not found")
            raise typer.Exit(1)

        if logo is not None:
            logo_size = Image.open(logo).size
        else:
            logo_size = (32, 32)

        os.makedirs("src", exist_ok=True)

        if logo is not None:
            os.makedirs("src/assets", exist_ok=True)
            shutil.copyfile(logo, os.path.join("src/assets", os.path.basename(logo)))

        manifest = {
            "manifest_version": 2,
            "name": name,
            "version": version,
            "description": description,
            "permissions": permissions,
            "background": {"scripts": ["background.js"]},
            "browser_action": {
                "default_icon": {logo_size[0]: f"assets/{os.path.basename(logo)}"},
                "default_title": browser_action_title,
            }
            if logo is not None
            else {
                "default_title": browser_action_title,
            },
            "browser_specific_settings": {
                "gecko": {"id": app_id, "strict_min_version": strict_min_version}
            },
        }

        with open("src/manifest.json", "w") as manifest_file:
            json.dump(manifest, manifest_file, indent=2)

        with open("src/background.js", "w") as background_file:
            background_file.write("")

        typer.echo(
            f"{bcolors.OKGREEN}Created {bcolors.OKCYAN}src/manifest.json{bcolors.ENDC}"
        )

    ask_for_input(False, None, None, None, None, None, None, None, None)


if __name__ == "__main__":
    app()
