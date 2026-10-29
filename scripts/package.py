"""Build local preparation directories and ZIPs; never upload or release."""
import argparse
import json

from plugin_tools import build_platform, load_platforms


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=["all", *load_platforms()], default="all")
    args = parser.parse_args()
    selected = load_platforms() if args.platform == "all" else [args.platform]
    for platform in selected:
        print(json.dumps(build_platform(platform), ensure_ascii=False))


if __name__ == "__main__":
    main()
