"""Validate one or all plugin packages locally; never call the service."""
import argparse

from plugin_tools import load_platforms, validate_platform


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=["all", *load_platforms()], default="all")
    args = parser.parse_args()
    selected = load_platforms() if args.platform == "all" else [args.platform]
    for platform in selected:
        manifest = validate_platform(platform)
        print(f'PASS: {platform}: {manifest["name"]} {manifest["version"]}; package validation only.')
    print("Host acceptance and marketplace status remain in platforms/<platform>/docs/.")


if __name__ == "__main__":
    main()
