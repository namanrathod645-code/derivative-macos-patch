# [ DC FORK ] Derivative 25.0.1 macOS patch

Community compatibility patch for **Derivative [25.0.1]** on macOS. Tested in Minecraft Java 1.21.11 with Fabric, Iris 1.10.7 and Sodium 0.8.7 on an Apple M2 Mac. The shader rendered in an isolated test world on 2026-09-29. Other hardware, dimensions, settings, and long sessions have not been verified.

This repository contains an installer and a small delta. It does **not** contain the original Derivative shader pack or its assets. Derivative remains the work of its original creators; this is an unofficial fork. The original pack is listed as **All Rights Reserved**.

## Install

1. Download **Derivative [25.0.1].zip** from the [Derivative [main] CurseForge page](https://www.curseforge.com/minecraft/shaders/derivative-main/files/all). Keep the ZIP unchanged.
2. With Python 3 installed, run:

   ```bash
   python3 apply_patch.py "/path/to/Derivative [25.0.1].zip"
   ```

3. Put the generated `Derivative-Mac-DC-FORK-25.0.1.zip` in Minecraft's `shaderpacks` folder. Select it in Iris's **Shader Packs** menu.

The installer checks the official ZIP's SHA-256 before changing anything. It refuses other versions or modified source archives. It does not modify your original ZIP. If Iris does not show the generated ZIP, extract it into its own folder in `shaderpacks` so that `shaders/` is directly inside that folder.

## What changed

- Adjusted unsupported GLSL version and qualifier syntax for macOS OpenGL 4.1.
- Selected the pack's existing fragment fallbacks for compute passes unavailable on stock macOS OpenGL.
- Moved random state initialization into runtime code to avoid an Apple OpenGL driver crash.
- Fixed shader compiler and linker issues found during live testing.

Some effects may differ from the original release. The patch targets only the exact 25.0.1 archive named above.

## Credits and rights

The original Derivative [main] project is by **DureXXX** and its team, including **M1zore** as lead pack developer. See the [official project page](https://www.curseforge.com/minecraft/shaders/derivative-main). The original archive's README requests the `[ DC FORK ]` label or a link to the original DERCODE for public forks. This repository does both.

The original pack's copyright and distribution terms remain with its creators. No permission to redistribute the complete original or modified pack is claimed here. If the creators request a change to this patch repository, open an issue.
