from telethon import TelegramClient
import asyncio
from telethon.sessions import StringSession
from telethon.tl.types import InputReplyToMessage
import os
import sys

API_ID = 611335
API_HASH = "d524b414d21f4d37f08684c1df41ac9c"

BETTER_NET = os.environ.get("BETTER_NET")
BBG = os.environ.get("BBG")
MOUNTIFY = os.environ.get("MOUNTIFY")
STOCK_CONFIG = os.environ.get("STOCK_CONFIG")
DROIDSPACES = os.environ.get("DROIDSPACES")
LTO = os.environ.get("LTO")
UNSHARE = os.environ.get("UNSHARE")
NTSYNC = os.environ.get("NTSYNC")
RESUKISU = os.environ.get("RESUKISU")
CVE_2026_43499 = os.environ.get("CVE_2026_43499")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))
RUN_URL = os.environ.get("RUN_URL")
BOT_CI_SESSION = os.environ.get("BOT_CI_SESSION")
MSG_TEMPLATE = """
**New Build Published!**
**LTO: {lto}**
```Kernel Info
kernelver: {kernelversion}
stock: {stock}
resukisu: {resukisu}
BBG: {bbg}
unshare: {unshare}
Mountify support: {mountify}
droidspaces: {droidspaces}
ntsync: {ntsync}
better net support: {better_net}
CVE-2026-43499 rtmutex fix: {cve_2026_43499}
```
Please follow @esk_gki_build !
#GKI2 #ESK
[Workflow run]({run_url})
""".strip()


def get_caption():
    msg = MSG_TEMPLATE.format(
        lto=LTO,
        kernelversion=get_kernel_versions(),
        stock=STOCK_CONFIG,
        unshare=UNSHARE,
        resukisu=RESUKISU,
        mountify=MOUNTIFY,
        droidspaces=DROIDSPACES,
        ntsync=NTSYNC,
        bbg=BBG,
        better_net=BETTER_NET,
        cve_2026_43499=CVE_2026_43499,
        run_url=RUN_URL,
    )
    return msg


def get_kernel_versions():
    version = ""
    patchlevel = ""
    sublevel = ""

    try:
        with open("./kernel_workspace/common/Makefile", 'r') as file:
            for line in file:
                if line.startswith("VERSION"):
                    version = line.split('=')[1].strip()
                elif line.startswith("PATCHLEVEL"):
                    patchlevel = line.split('=')[1].strip()
                elif line.startswith("SUBLEVEL"):
                    sublevel = line.split('=')[1].strip()
                elif line.startswith("#"):  # skip comments
                    continue
                else:
                    break
    except FileNotFoundError:
        raise
    return f"{version}.{patchlevel}.{sublevel}"


async def send_telegram_message(file_path: str):
    async with TelegramClient(StringSession(BOT_CI_SESSION), api_id=API_ID, api_hash=API_HASH) as client:
        await client.start(bot_token=BOT_TOKEN)
        print("[+] Caption: ")
        print("---")
        print("---")
        print("[+] Sending")
        await client.send_file(
            entity=CHAT_ID,
            file=file_path,
            parse_mode="markdown",
            caption=get_caption(),
        )

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)

    file_to_upload = sys.argv[1]
    if not os.path.isfile(file_to_upload):
        print(f"Error: {file_to_upload} does not exist!")
        sys.exit(1)

    asyncio.run(send_telegram_message(file_to_upload))
