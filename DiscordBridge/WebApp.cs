using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;
using System.Net.WebSockets;
using System.Text;
using System.Threading.Channels;

namespace DiscordBridge
{
    public class WebApp
    {
        private readonly WebApplicationBuilder builder;
        private WebApplication? app;

        private readonly Channel<WebSocketMessage> messageChannel = Channel.CreateUnbounded<WebSocketMessage>();
        private readonly List<WebSocket> clients = new();

        // Подписка на входящие сообщения
        public event Action<WebSocket, string>? OnMessageReceived;

        public WebApp()
        {
            builder = WebApplication.CreateBuilder();
            builder.Services.AddRouting();
        }

        public void Build()
        {
            app = builder.Build();

            app.UseWebSockets();
            app.Use(async (context, next) =>
            {
                if (context.WebSockets.IsWebSocketRequest)
                {
                    var webSocket = await context.WebSockets.AcceptWebSocketAsync();
                    clients.Add(webSocket);
                    await HandleWebSocket(context, webSocket);
                }
                else
                {
                    await next(context);
                }
            });
        }

        private async Task HandleWebSocket(HttpContext context, WebSocket webSocket)
        {
            var buffer = new byte[1024 * 4];

            while (webSocket.State == WebSocketState.Open)
            {
                var result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);

                if (result.MessageType == WebSocketMessageType.Close)
                {
                    clients.Remove(webSocket);
                    await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closed by client", CancellationToken.None);
                    break;
                }

                var msg = Encoding.UTF8.GetString(buffer, 0, result.Count);
                var socketMessage = new WebSocketMessage
                {
                    Context = context,
                    WebSocket = webSocket,
                    Message = msg
                };

                await messageChannel.Writer.WriteAsync(socketMessage);
            }
        }

        public void Map(string pattern, Func<HttpContext, Task> callback)
        {
            app!.Map(pattern, callback);
        }

        public void MapGet(string pattern, Func<HttpContext, Task> callback)
        {
            if (!IsAppValid()) return;
            app!.MapGet(pattern, callback);
        }

        public void MapPost(string pattern, Func<HttpContext, Task> callback)
        {
            if (!IsAppValid()) return;
            app!.MapPost(pattern, callback);
        }

        public void Run(string? url = "http://localhost:5000")
        {
            if (!IsAppValid())
                throw new Exception("App is not built. Run Build() first.");

            _ = Task.Run(ProcessWebSocketMessages);

            app!.Run(url);
        }

        public async Task BroadcastAsync(string message)
        {
            var bytes = Encoding.UTF8.GetBytes(message);
            var segment = new ArraySegment<byte>(bytes);

            foreach (var ws in clients.ToList())
            {
                if (ws.State == WebSocketState.Open)
                {
                    await ws.SendAsync(segment, WebSocketMessageType.Text, true, CancellationToken.None);
                }
            }
        }

        private bool IsAppValid() => app != null;

        private async Task ProcessWebSocketMessages()
        {
            await foreach (var message in messageChannel.Reader.ReadAllAsync())
            {
                Console.WriteLine($"[WS] Received message: {message.Message}");

                OnMessageReceived?.Invoke(message.WebSocket, message.Message);
            }
        }

        private class WebSocketMessage
        {
            public required HttpContext Context { get; init; }
            public required WebSocket WebSocket { get; init; }
            public required string Message { get; init; }
        }
    }
}
