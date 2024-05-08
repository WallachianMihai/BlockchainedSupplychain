namespace NodeClient.Data.Model;

public class Contract
{
    public int Id { get; init; }
    public int Product_id { get; init; }
    public string Customer_id { get; init; } = null!;
    public int Quantity { get; init; }
    public string Contract_path { get; init; } = null!;
}
