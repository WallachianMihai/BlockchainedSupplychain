using System.Text;
using System.Text.Json;
using Humanizer;
using NodeClient.Data.Model;

namespace NodeClient.Extensions;

public class NodeService : INodeService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger _logger;


    public NodeService(HttpClient httpClient, ILogger<NodeService> logger)
    {
        _httpClient = httpClient;
        _logger = logger;

        _httpClient.BaseAddress = new Uri("http://localhost:8001/");
    }

    public async Task<IEnumerable<Company>?> GetCompaniesAsync() =>
        await _httpClient.GetFromJsonAsync<IEnumerable<Company>>("customers");

    public async Task<IEnumerable<Contract>?> GetContractsAsync() =>
        await _httpClient.GetFromJsonAsync<IEnumerable<Contract>>("contracts");

    public async Task<IEnumerable<Inventory>?> GetInventoryAsync() =>
        await _httpClient.GetFromJsonAsync<IEnumerable<Inventory>>("inventory");

    public async Task<IEnumerable<Product>?> GetProductsAsync() =>
        await _httpClient.GetFromJsonAsync<IEnumerable<Product>>("products");

    public async Task<Tuple<bool, bool>?> GetContractFulfilmentAsync(int contractId)
    {
        return await _httpClient.GetFromJsonAsync<Tuple<bool, bool>>($"contract-fulfilment/{contractId}");
    }

    public async Task<IEnumerable<string>?> GetContractTrailAsync(int contractId)
    {
        return await _httpClient.GetFromJsonAsync<IEnumerable<string>>($"contract-trail/{contractId}");
    }
    
    public async Task<ContractData?> GetContractDataAsync(int contractId)
    {
        return await _httpClient.GetFromJsonAsync<ContractData>($"contract-data/{contractId}");
    }
    
    public async Task<HttpResponseMessage> StartNewContractAsync(Company supplier, Product product, int quatinty,
        string account)
    {
        string client_name = (await GetCompaniesAsync()).Where(c => c.Account == account).First().Name;
        
        var content = new StartContract
        {
            ClientAccount = account,
            Client = client_name,
            ProductId = product.Id,
            Product = product.Name,
            Quantity = quatinty,
            Seller = supplier.Name,
            SellerAccount = supplier.Account,
        };
        
        var body = JsonSerializer.Serialize(content);
        _logger.LogInformation($"POST start-contract; body: {body}");
        
        var requestContent = new StringContent(body, Encoding.UTF8, "application/json");

        return await _httpClient.PostAsync("start-contract", requestContent);
    }

    public async Task<HttpResponseMessage> HandoverAsync(int contractId, string accountFrom, string accountTo)
    {
        var content = new Dictionary<string, string>
        {
            { "from", accountFrom },
            { "to", accountTo }
        };
        
        var body = JsonSerializer.Serialize(content);
        _logger.LogInformation($"POST handover/{contractId}; body: {body}");
        
        var requestContent = new StringContent(body, Encoding.UTF8, "application/json");
        
        return await _httpClient.PostAsync($"handover/{contractId}", requestContent);
    }

    public async Task<HttpResponseMessage> ReceiveAsync(int contractId, string accountFrom)
    {
        var body = JsonSerializer.Serialize(new { from = accountFrom });

        _logger.LogInformation($"POST receive/{contractId}; body: {body}");
        
        var requestContent = new StringContent(body, Encoding.UTF8, "application/json");
        
        return await _httpClient.PostAsync($"receive/{contractId}", requestContent);
    }
    
    public async Task<HttpResponseMessage> EndContractAsync(int contractId, string accountFrom)
    {
        var body = JsonSerializer.Serialize(new { account = accountFrom });

        _logger.LogInformation($"POST end-contract/{contractId}; body: {body}");
        
        var requestContent = new StringContent(body, Encoding.UTF8, "application/json");
        
        return await _httpClient.PostAsync($"end-contract/{contractId}", requestContent);
    }
}