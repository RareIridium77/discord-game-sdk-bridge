using System.Text.Json.Serialization;
using DiscordActivityType = Discord.ActivityType;

namespace DiscordBridge.Models
{
    public class ActivityPayload
    {
        [JsonConverter(typeof(JsonStringEnumConverter))]
        public DiscordActivityType Type { get; set; }
        public string? Name { get; set; }
        public string? State { get; set; }
        public string? Details { get; set; }

        public long? StartTimestamp { get; set; }
        public long? EndTimestamp { get; set; }

        public string? LargeImage { get; set; }
        public string? LargeImageText { get; set; }
        public string? SmallImage { get; set; }
        public string? SmallImageText { get; set; }

        public ActivityParty? Party { get; set; }
        public ActivitySecrets? Secrets { get; set; }

        public bool Instance { get; set; }
    }

    public class ActivityParty
    {
        public string? Id { get; set; }
        public int? CurrentSize { get; set; }
        public int? MaxSize { get; set; }
    }

    public class ActivitySecrets()
    {
        public string? Join { get; set; }
        public string? Match { get; set; }
        public string? Spectate { get; set; }
    }
}
