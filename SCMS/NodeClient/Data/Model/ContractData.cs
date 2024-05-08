using System.Text.Json.Serialization;

namespace NodeClient.Data.Model;

public class ContractData
{
    [JsonPropertyName("seller")]
    public string Seller { get; set; }
    
    [JsonPropertyName("holder")]
    public string Holder { get; set; }
    
    [JsonPropertyName("next_holder")]
    public int NextHolder { get; set; }
    
    [JsonPropertyName("client")]
    public string Client { get; set; }
    
    [JsonPropertyName("product")]
    public int Product { get; set; }
    
    [JsonPropertyName("quantity")]
    public int Quantity { get; set; }
}