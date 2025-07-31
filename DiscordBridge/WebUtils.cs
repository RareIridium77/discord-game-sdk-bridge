

using System.Text.Json;
using Microsoft.AspNetCore.Http;

namespace DiscordBridge
{
    public static class WebUtils
    {
        private static JsonSerializerOptions defaultOptions = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };
        
        public static async Task<T?> DeserializeJson<T>(HttpContext context, JsonSerializerOptions? options = null)
        {
            try
            {
                if (options == null) options = defaultOptions;
                
                return await JsonSerializer.DeserializeAsync<T>(context.Request.Body, options);
            }
            catch
            {
                context.Response.StatusCode = 400;
                await context.Response.WriteAsync("Invalid or malformed JSON.");
                return default;
            }
        }
    }
}