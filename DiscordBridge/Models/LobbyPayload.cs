using System.Text.Json.Serialization;
using DiscordActivityActionType = Discord.ActivityActionType;
using DiscordActivityJoinRequestReply = Discord.ActivityJoinRequestReply;

namespace DiscordBridge.Models
{
    public class Invite
    {
        public long UserId { get; set; }

        [JsonConverter(typeof(JsonStringEnumConverter))]
        public DiscordActivityActionType ActivityActionType { get; set; }
        public string? Content { get; set; }
    }

    public class InviteAccept
    {
        public long UserId { get; set; }
    }

    public class JoinRequestReply
    {
        public long UserId { get; set; }

        [JsonConverter(typeof(JsonStringEnumConverter))]
        public DiscordActivityJoinRequestReply ActivityJoinRequestReply { get; set; }
    }
}
