/*

    Welcome
    Discord Bridge

*/

using DiscordBridge;
using DotNetEnv; // `dotnet add package DotNetEnv`

try
{
    Env.Load(Path.Combine(AppContext.BaseDirectory, ".env"));
    Console.WriteLine("Trying to load .env file");
}
catch (Exception e)
{
    Console.WriteLine($"[?] .env file not found or not readen: {e.Message}");
}

string? GetArg(string[] args, string key, string? fallback = null)
{
    var index = Array.IndexOf(args, key);
    if (index >= 0 && index + 1 < args.Length)
    {
        return args[index + 1];
    }
    return fallback;
}

string? rawClientId = Env.GetString("DISCORD_SDK_CLIENT_ID", GetArg(args, "--clientId", "-1"));
string? url = Env.GetString("DISCORD_SDK_HOST", GetArg(args, "--host") ?? "http://localhost:5000");

long clientId = long.TryParse(rawClientId, out var cid) ? cid : -1;

if (clientId <= 0)
{
    Console.WriteLine("[!] Invalid or missing --clientId argument is required. Or add it on .env file with key DISCORD_SDK_CLIENT_ID");
    Console.WriteLine("Press any key to exit...");
    Console.ReadKey();
    return;
}

Console.WriteLine($"[*] Launching DiscordBridge with clientId={clientId}, host={url}");

var server = new DiscordBridgeServer(clientId, url);
await server.StartAsync();
