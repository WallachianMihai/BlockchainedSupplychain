using System.Text.Json.Serialization;

namespace NodeClient.Data.Model;

public class TransferProductEvent
{
    [JsonPropertyName("holder")]
    public string Holder { get; set; }
    
    [JsonPropertyName("new_holder")]
    public string NewHolder { get; set; }
    
    [JsonPropertyName("agreement_id")]
    public int AgreementId { get; set; }
}