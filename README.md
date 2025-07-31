# discord-game-sdk-bridge

A lightweight REST + WebSocket bridge for the [Discord Game SDK](https://discord.com/developers/docs/developer-tools/game-sdk), enabling Discord Rich Presence and activity features via Python or other languages.

> ⚠️ After building the executable, do not forget to place `discord_game_sdk.dll` next to it.  
> You can find it here: https://discord.com/developers/docs/developer-tools/game-sdk

---

## Status

**WIP** and just a for-fun project.  
I built this while I was bored.

---

## Dependencies

This project uses the following NuGet packages:

- [DotNetEnv (v3.1.1)](https://www.nuget.org/packages/DotNetEnv)
- [Microsoft.AspNetCore.App (v2.2.8)](https://www.nuget.org/packages/Microsoft.AspNetCore.App)

> These should restore automatically via `dotnet restore`, but feel free to install them manually if needed.

---

## Getting Started

```bash
git clone https://github.com/RareIridium77/discord-game-sdk-bridge.git
cd discord-game-sdk-bridge/DiscordBridge
dotnet build
```

then drop `discord_game_sdk.dll` next to built executable.

# Licence
MIT
