namespace NodeClient.Data.Model;

public class Product
{
    public int Id { get; init; }
    public string Name { get; init; } = null!;
    public string Description { get; init; } = null!;
    public float Price { get; init; }
}
