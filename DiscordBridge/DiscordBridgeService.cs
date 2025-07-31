using Discord;

namespace DiscordBridge
{
    public class DiscordBridgeService
    {
        private readonly Discord.Discord discord;
        public readonly ActivityManager activityManager;
        private Activity? lastActivity;

        // private 

        public DiscordBridgeService(long clientId)
        {
            discord = new Discord.Discord(
                clientId,
                (ulong)CreateFlags.NoRequireDiscord
            );

            activityManager = discord.GetActivityManager();
        }

        private CancellationTokenSource? callbackTokenSource;

        public void StartCallbackLoop()
        {
            callbackTokenSource = new CancellationTokenSource();

            _ = Task.Run(async () =>
            {
                var token = callbackTokenSource.Token;
                try
                {
                    while (!token.IsCancellationRequested)
                    {
                        discord.RunCallbacks();
                        await Task.Delay(500, token);
                    }
                }
                catch (OperationCanceledException)
                {
                    Console.WriteLine("[!] Callback loop cancelled.");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"[!] Callback loop error: {ex.Message}");
                }
            }, callbackTokenSource.Token);
        }

        public void StopCallbackLoop()
        {
            callbackTokenSource?.Cancel();
            callbackTokenSource?.Dispose();
            callbackTokenSource = null;
        }

        public void DisplayPayload(Models.ActivityPayload payload)
        {
            Console.WriteLine("Payload debug:");
            Console.WriteLine($"Type: {payload.Type}");
            Console.WriteLine($"Name: {payload.Name}");
            Console.WriteLine($"State: {payload.State}");
            Console.WriteLine($"Details: {payload.Details}");
            Console.WriteLine($"StartTimestamp: {payload.StartTimestamp}");
            Console.WriteLine($"EndTimestamp: {payload.EndTimestamp}");
            Console.WriteLine($"LargeImageKey: {payload.LargeImage}");
            Console.WriteLine($"LargeImageText: {payload.LargeImageText}");
            Console.WriteLine($"SmallImageKey: {payload.SmallImage}");
            Console.WriteLine($"SmallImageText: {payload.SmallImageText}");
            Console.WriteLine($"Instance: {payload.Instance}");

            if (payload.Party != null)
            {
                Console.WriteLine("Party:");
                Console.WriteLine($"  Id: {payload.Party.Id}");
                Console.WriteLine($"  CurrentSize: {payload.Party.CurrentSize}");
                Console.WriteLine($"  MaxSize: {payload.Party.MaxSize}");
            }
            else
            {
                Console.WriteLine("Party: null");
            }

            if (payload.Secrets != null)
            {
                Console.WriteLine("Secrets:");
                Console.WriteLine($"  Join: {payload.Secrets.Join}");
                Console.WriteLine($"  Match: {payload.Secrets.Match}");
                Console.WriteLine($"  Spectate: {payload.Secrets.Spectate}");
            }
            else
            {
                Console.WriteLine("Secrets: null");
            }
        }

        public void UpdateActivity(Models.ActivityPayload payload)
        {
            var activity = new Activity
            {
                Type = payload.Type,
                Name = payload.Name ?? "",
                State = payload.State ?? "",
                Details = payload.Details ?? "",
                Timestamps =
                {
                    Start = payload.StartTimestamp
                        ?? lastActivity?.Timestamps.Start
                        ?? DateTimeOffset.Now.ToUnixTimeSeconds(),

                    End = payload.EndTimestamp ?? 0
                },
                Assets =
                {
                    LargeImage = payload.LargeImage ?? "",
                    LargeText = payload.LargeImageText ?? "",
                    SmallImage = payload.SmallImage ?? "",
                    SmallText = payload.SmallImageText ?? ""
                },
                Instance = payload.Instance,
            };

            if (payload.Party != null)
            {
                activity.Party = new ActivityParty
                {
                    Id = payload.Party.Id ?? "",
                    Size = new PartySize
                    {
                        CurrentSize = payload.Party.CurrentSize ?? 0,
                        MaxSize = payload.Party.MaxSize ?? 0
                    }
                };
            }

            if (payload.Secrets != null)
            {
                activity.Secrets = new ActivitySecrets
                {
                    Join = payload.Secrets.Join ?? "",
                    Match = payload.Secrets.Match ?? "",
                    Spectate = payload.Secrets.Spectate ?? ""
                };
            }

            // DisplayPayload(payload);

            activityManager.UpdateActivity(activity, result =>
            {
                Console.WriteLine(result == Result.Ok
                    ? "[+] Activity updated!"
                    : $"[-] Failed to update activity: {result}");
            });
        }
    }
}
