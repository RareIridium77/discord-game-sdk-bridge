using Discord;
using Microsoft.AspNetCore.Http;
using System.Text.Json;

namespace DiscordBridge
{
    public class DiscordBridgeServer
    {
        private readonly WebApp webApp;
        private readonly DiscordBridgeService discordService;
        private readonly ActivityManager activityManager;
        private readonly string url;

        /// <summary>
        /// Basic Json serializing options
        /// </summary>
        JsonSerializerOptions options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };

        /// <summary>
        /// Builds web application and discord service
        /// </summary>
        /// <param name="clientId">application id</param>
        /// <param name="url">host url</param>
        /// <exception cref="Exception">clientId is not valid</exception>
        public DiscordBridgeServer(long clientId, string url = "ws://localhost:5000")
        {
            if (clientId == -1)
            {
                throw new Exception("clientId is not valid");
            }

            this.url = url;
            this.webApp = new WebApp();
            this.discordService = new DiscordBridgeService(clientId);
            this.activityManager = discordService.activityManager;

            webApp.Build();

            RegisterRoutes();
            RegisterOnCallbacks();

            // TODO: 
            // activityManager.RegisterCommand(string? command = null)
            // activityManager.RegisterSteam(uint steamId)
        }

        private void Log(string message) => Console.WriteLine($"[DiscordBridge] {message}");

        /// <summary>
        /// Sends websocket event to clients.
        /// </summary>
        /// <param name="eventName">name of the event</param>
        /// <param name="payload">data of the event</param>
        /// <returns></returns>
        private async Task SendEvent(string eventName, object payload)
        {
            var json = JsonSerializer.Serialize(new
            {
                @event = eventName,
                data = payload
            }, options);

            Log("[WS] Broadcasting:");
            Log(json);

            await webApp.BroadcastAsync(json);
        }

        /// <summary>
        /// Request handler.
        /// </summary>
        /// <param name="context">HttpContext</param>
        /// <param name="handler">Function to handle</param>
        /// <returns></returns>
        private async Task HandleRequest(HttpContext context, Func<Task> handler)
        {
            try
            {
                await handler();
            }
            catch (Exception ex)
            {
                Log($"[-] Exception: {ex.Message}");
                context.Response.StatusCode = 500;
                await context.Response.WriteAsync("Internal server error.");
            }
        }

        /// <summary>
        /// I Lost My Mind
        /// </summary>
        /// <param name="context"></param>
        /// <param name="result"></param>
        /// <returns></returns>
        private async Task HandleDiscordResult(HttpContext context, Result result)
        {
            int resultCode = (int)result;
            string resultName = result.ToString();

            if (result == Result.Ok)
            {
                await context.Response.WriteAsync(resultName);
            }
            else
            {
                context.Response.StatusCode = resultCode;
                await context.Response.WriteAsync($"Error: {resultName} ({resultCode})");
            }
        }

        bool discordServiceEnabled = true;

        private void EnableDiscordService()
        {
            if (!discordServiceEnabled)
            {
                discordService.StartCallbackLoop();
                discordServiceEnabled = true;
                Log("[+] Discord service enabled.");
            }
            else
            {
                Log("[=] Discord service already enabled.");
            }
        }

        private void DisableDiscordService()
        {
            if (discordServiceEnabled)
            {
                discordService.StopCallbackLoop();
                discordServiceEnabled = false;
                Log("[−] Discord service disabled.");
            }
            else
            {
                Log("[=] Discord service already disabled.");
            }
        }

        /// <summary>
        /// discord service callbacks.
        /// </summary>
        private void RegisterOnCallbacks()
        {
            activityManager.OnActivityJoin += async secret =>
            {
                Log($"[+] Join secret received: {secret}");
                await SendEvent("join", secret);
            };

            activityManager.OnActivitySpectate += async secret =>
            {
                Log($"[+] Spectate secret: {secret}");
                await SendEvent("spectate", secret);
            };

            activityManager.OnActivityJoinRequest += (ref User user) =>
            {
                var userId = user.Id;
                var name = user.Username;
                var discr = user.Discriminator;
                var userBot = user.Bot;
                var userAvatar = user.Avatar;

                Log($"[+] Join request from: {user.Username}");

                Task.Run(async () =>
                {
                    await SendEvent("join-request", new
                    {
                        id = userId,
                        username = name,
                        discriminator = discr,
                        isBot = userBot,
                        avatar = userAvatar,
                    });
                });
            };
        }

        /// <summary>
        /// Makes basic routes.
        /// </summary>
        private void RegisterRoutes()
        {
            webApp.MapGet("/", async context =>
            {
                await context.Response.WriteAsync("Hello from DiscordBridge!");
            });

            webApp.MapPost("/enable_discord", async context =>
            {
                EnableDiscordService();
                await context.Response.WriteAsync("Discord service enabled.");
            });

            webApp.MapPost("/disable_discord", async context =>
            {
                DisableDiscordService();
                await context.Response.WriteAsync("Discord service disabled.");
            });

            webApp.MapPost("/accept_invite", async context =>
            {
                await HandleRequest(context, async () =>
                {
                    var payload = await WebUtils.DeserializeJson<Models.InviteAccept>(context);
                    if (payload == null) return;

                    Log(payload.ToString());

                    var tcs = new TaskCompletionSource<Result>();

                    activityManager.AcceptInvite(payload.UserId, result =>
                    {
                        tcs.SetResult(result);
                    });

                    var finalResult = await tcs.Task;
                    await HandleDiscordResult(context, finalResult);
                });
            });

            webApp.MapPost("/send_invite", async context =>
            {
                await HandleRequest(context, async () =>
                {
                    var payload = await WebUtils.DeserializeJson<Models.Invite>(context);
                    if (payload == null) return;

                    Log(payload.ToString());

                    var tcs = new TaskCompletionSource<Result>();

                    activityManager.SendInvite(payload.UserId, payload.ActivityActionType, payload.Content, result =>
                    {
                        tcs.SetResult(result);
                    });

                    var finalResult = await tcs.Task;
                    await HandleDiscordResult(context, finalResult);
                });
            });

            webApp.MapPost("/test_ws", async context =>
            {
                await SendEvent("spectate", "Hello from bridge");
            });

            webApp.MapPost("/send_request_reply", async context =>
            {
                await HandleRequest(context, async () =>
                {
                    var payload = await WebUtils.DeserializeJson<Models.JoinRequestReply>(context);
                    if (payload == null) return;

                    Log(payload.ToString());

                    var tcs = new TaskCompletionSource<Result>();

                    activityManager.SendRequestReply(payload.UserId, payload.ActivityJoinRequestReply, result =>
                    {
                        tcs.SetResult(result);
                    });

                    var finalResult = await tcs.Task;
                    await HandleDiscordResult(context, finalResult);
                });
            });

            webApp.MapPost("/set_activity", async context =>
            {
                await HandleRequest(context, async () =>
                {
                    var payload = await WebUtils.DeserializeJson<Models.ActivityPayload>(context);
                    if (payload == null) return;

                    Log(payload.ToString());
                    discordService.UpdateActivity(payload);

                    await context.Response.WriteAsync("Activity set.");
                });
            });

            webApp.MapPost("/clear_activity", async context =>
            {
                await HandleRequest(context, async () =>
                {
                    activityManager.ClearActivity(result =>
                    {
                        Log(result == Result.Ok
                            ? "[+] Activity cleared."
                            : $"[!] Failed to clear activity: {result}");
                    });

                    await context.Response.WriteAsync("Activity cleared");
                });
            });
        }

        /// <summary>
        /// Starts everything
        /// </summary>
        /// <returns></returns>
        public async Task StartAsync()
        {
            discordService.StartCallbackLoop();

            AppDomain.CurrentDomain.ProcessExit += (_, _) =>
            {
                discordService.StopCallbackLoop();
            };

            webApp.Run(url);
            await Task.CompletedTask;
        }
    }
}
