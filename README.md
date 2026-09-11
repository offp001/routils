# 🛠️ RoUtils (Version 3.7)

## Features

### Cache Editor

* **3D preview** – View cached Roblox meshes and models directly inside RoUtils
* **Image preview** – Preview cached PNG/image assets
* **Audio preview** – Preview cached OGG/MP3 assets
* **Dump** – Dump Roblox cache files into organized folders
* **Export** – Export individual cache files in different formats
* `Full Blob`
* `RBXM`
* `Image`
* `Copy / Save Hash`
* **Delete Cache Type** – Delete a selected cache category

#### How does Cache Editor work?

RoUtils reads the cache data created by the Roblox client and organizes the available cache files into categories.

When you open the **Cache** tab, RoUtils scans the Roblox cache database and identifies the available cached assets. Depending on the asset type, RoUtils can display additional information or provide a preview.

Cached files are separated into categories such as:

* Mesh
* Model / RBXM
* Animation
* Image
* Audio
* Font
* Text
* Unknown

You can select a cache entry to inspect it. Supported assets can be previewed directly in RoUtils, including 3D models, images and audio files.

**Dump Caches** can be used when you want to extract cached files from the Roblox cache and store them in the RoUtils Dump folder. The dumped files are organized by category so they are easier to find.

The **Export** options allow you to export a selected cache entry in the format you need:

* **Full Blob** – Export the complete cache blob
* **RBXM** – Export compatible Roblox model data
* **Image** – Export image assets
* **Copy / Save Hash** – Copy or save the cache hash for later use

The **Delete Cache Type** option allows you to remove an entire category of cached data. For example, selecting `Image` will remove cached image data without requiring you to manually find each individual file.

RoUtils performs cache operations without intentionally blocking the main interface, so large cache operations should remain responsive.

---

### FFlag Manager

* **FFlag Injector** – Apply FFlags into Roblox
* **Saved JSONs** – Save and load FFlag JSON configurations
* **Hotkeys** – Apply/Change Values using Hotkeys
* **Presets** – Load FFlag presets from the RoUtils GitHub
* **JSON Editor** – Edit FFlag JSON files directly
* **Default FFlag Values** – Open the default FFlag values
* **Latest FFlag List** – Open the latest FFlag list

#### How does FFlag Manager work?

FFlags (Fast Flags) are configuration values used by Roblox to control different client behaviors and features.

RoUtils provides a dedicated interface for creating, editing and applying FFlag configurations instead of requiring you to manually edit configuration files.

The basic workflow is:

**FFlags → JSON Editor → Paste your JSON → Add → Apply**

You can open **JSON Editor** and paste an FFlag configuration in JSON format. After adding it, the configuration can be applied through RoUtils.

Example:

```json
{
    "FFlagExample": "True"
}
```

RoUtils also creates a `jsons` folder where saved `.json` configurations can be stored. These files appear inside the FFlag Manager, allowing you to select a configuration and apply it later without having to paste the JSON again.

**Saved JSONs** are useful if you have different configurations for different purposes. You can keep multiple configurations and switch between them whenever necessary.

**Presets** provide ready-made FFlag configurations from the RoUtils GitHub repository. Presets can be added to your current FFlag configuration instead of requiring you to manually copy every value.

**Hotkeys** allow supported FFlag values to be changed or applied using configured keyboard shortcuts.

**Default FFlag Values** opens the default Roblox FFlag values list.

**Latest FFlag List** provides a list of currently tracked FFlags so you can inspect available names and values.

---

### 🛠️ Modifications

* **Default R6 Mesh Changer** – Change default R6 character meshes
* **Mesh to OBJ Converter** – Convert meshes to OBJ format
* **File Converter** – Convert `.rbxm` / `.rbxmx` / `.rbxh` files
* **RBXM → RBXH Blob** – Convert RBXM to RBXH v2 cache blobs
* **R6 to R15 Animations** – Convert R6 animations to R15 animations

### CConfigs (.db configs)

* **Save `rbx-storage.db` file**

### Subplace Joiner

* **Subplace Joiner** – Join Roblox subplaces by entering a Universe ID or Place ID
* **Copy Deep Link** – Copy the current server deeplink

#### How does Subplace Joiner work?

A Roblox experience can contain multiple places. These additional places are commonly referred to as **subplaces**.

The **Subplace Joiner** allows you to join a specific Roblox place by entering its **Place ID** or using the relevant **Universe ID** information.

Instead of opening the main experience and navigating through it manually, you can enter the ID of the place you want to join and let RoUtils generate the appropriate Roblox deep link.

### Place ID vs Universe ID

**Place ID** identifies a specific Roblox place.

For example, a game can have:

* A main lobby
* A map
* A loading place
* A trading place
* A different game mode

Each of these can have its own Place ID.

**Universe ID** identifies the overall Roblox experience and can contain multiple places.

If you already know the **Place ID** of the subplace you want to enter, you can enter it directly into the Subplace Joiner.

After generating the join link, **Copy Deep Link** can be used to copy the Roblox deep link to your clipboard.

> 💡 If a game contains multiple places, the Place ID is the important value when you want to target a specific subplace.

---

### Server Viewer

* **See server information without joining with deeplink**

  * Place ID
  * Job ID
  * Players
  * Max Capacity
  * Ping
  * Server FPS
  * Location

#### How does Server Viewer work?

The **Server Viewer** lets you inspect Roblox public server information without first joining the server.

You can provide the game's **Place ID** and the server's **Job ID** to identify a specific server.

### What is a Job ID?

A **Job ID** is the unique identifier of a running Roblox server instance.

A Place ID identifies the game/place itself, while a Job ID identifies a particular server running that place.

For example:

```text
Place ID:
123456789

Job ID:
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

There can be many servers running the same Place ID at the same time. Each server has its own Job ID.

This means:

```text
Place ID = Which game/place?
Job ID   = Which server?
```

After providing the required information, Server Viewer can display available server information such as:

* **Place ID** – The Roblox place being hosted
* **Job ID** – The unique server instance ID
* **Players** – Current number of players in the server
* **Max Capacity** – Maximum player capacity
* **Ping** – Reported server/network latency
* **Server FPS** – Server-side performance information
* **Location** – Server location/region when available

The purpose of Server Viewer is to let you inspect a server before deciding whether you want to join it.

---

### History

* **Game History** – Save game history and join games again later
* **Server History** – Keep recently visited servers and join them again

### Client

* **Client Information** – Show CPU/RAM usage and current Game ID/JobID
* **FPS Changer** – Change Roblox's FPS limit
* **FPS Hotkeys** – Change Roblox's FPS limit using Hotkeys

### Themes

* **25 Themes** – Midnight, Ocean, Hacker, Amethyst, Onyx, Nord, Dracula, Monokai, Solarized, Rose Pine, Catppuccin, Gruvbox, Tokyo Night, Synthwave, Forest, Ruby, Amber, Arctic, Lavender, Coffee, Slate, Cyber, Sunset, Mint, Deep Blue
* **Custom Theme** – Create your own custom color theme

### RoUtils AI

* **RoUtils AI Chat** – Ask questions directly inside RoUtils (Add Gemini API Key on settings to use) (Powered by Gemini AI)

### Windows / Startup

* **System Tray** – Run RoUtils from the Windows notification area
* **Launch on Tray** – Start RoUtils directly in the system tray
* **Hide to Tray when Close** – Closing the main window can keep RoUtils running in the tray
* **Open / Exit from Tray** – Tray menu provides Open and Exit controls

## Installation

1. Open `RoUtils.exe`
2. Done :) (easy right?)

## Credits

* `offp001` (If you encounter any issues, feel free to contact me on Discord👍)
