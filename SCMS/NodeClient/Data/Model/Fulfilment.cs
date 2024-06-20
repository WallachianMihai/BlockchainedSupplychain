using System.Text.Json.Serialization;

namespace NodeClient.Data.Model;

public class Fulfilment
{
    [JsonPropertyName("client")]
    public bool Client { get; set; }
    [JsonPropertyName("seller")]
    public bool Seller { get; set; }
}