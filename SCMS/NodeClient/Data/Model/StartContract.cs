using System.Text.Json.Serialization;

namespace NodeClient.Data.Model;

public class StartContract
{
    [JsonPropertyName("account_client")]
    public string ClientAccount { get; set; }
    
    [JsonPropertyName("client")]
    public string Client { get; set; }
    
    [JsonPropertyName("product_id")]
    public int ProductId { get; set; }
    
    [JsonPropertyName("product")]
    public string Product { get; set; }
    
    [JsonPropertyName("quantity")]
    public int Quantity { get; set; }
    
    [JsonPropertyName("seller")]
    public string Seller { get; set; }
    
    [JsonPropertyName("account_seller")]
    public string SellerAccount { get; set; }
}