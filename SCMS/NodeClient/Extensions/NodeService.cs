using System.Text;
using System.Text.Json;
using Humanizer;
using Microsoft.AspNetCore.SignalR;
using NodeClient.Data.Model;

namespace NodeClient.Extensions;

public class NodeService : INodeService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger _logger;
    private readonly IHubContext<TransferHub, INotificationClient> _hubContext;

    public NodeService(HttpClient httpClient, ILogger<NodeService> logger, IHubContext<TransferHub, INotificationClient> hubContext)
    {
        _httpClient = httpClient;
        _logger = logger;
        _hubContext = hubContext;

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

    public async Task<Fulfilment?> GetContractFulfilmentAsync(int contractId)
    {
        return await _httpClient.GetFromJsonAsync<Fulfilment>($"contract-fulfilment/{contractId}");
    }

    public async Task<IEnumerable<Company>?> GetContractTrailAsync(int contractId)
    {
        var trail = await _httpClient.GetFromJsonAsync<IEnumerable<string>>($"contract-trail/{contractId}");
        var companies = await _httpClient.GetFromJsonAsync<IEnumerable<Company>>("customers");

        List<Company> nodes = new List<Company>();
        
        foreach (var node in trail)
        {
            nodes.Add(companies.First(c => c.Account == node));
        }

        return nodes;
    }
    
    public async Task<ContractData?> GetContractDataAsync(int contractId)   
    {
        return await _httpClient.GetFromJsonAsync<ContractData>($"contract-data/{contractId}");
    }

    public async Task GetEvents()
    {
        var result = await _httpClient.GetFromJsonAsync<TransferProductEvent>($"events");
        await _hubContext.Clients.All.ReceiveTransferDetails(result);
        _logger.LogInformation($"{result.AgreementId}, {result.NewHolder}, {result.Holder}");
    }
    
    public async Task<ApiFailedResponse> StartNewContractAsync(Company supplier, Product product, int quatinty,
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

        var result = await _httpClient.PostAsync("start-contract", requestContent);
        return await result.Content.ReadFromJsonAsync<ApiFailedResponse>();
    }

    public async Task<ApiFailedResponse> HandoverAsync(int contractId, string accountFrom, string accountTo)
    {
        var content = new Dictionary<string, string>
        {
            { "from", accountFrom },
            { "to", accountTo }
        };
        
        var body = JsonSerializer.Serialize(content);
        _logger.LogInformation($"POST deliver/{contractId}; body: {body}");
        
        var requestContent = new StringContent(body, Encoding.UTF8, "application/json");
        
        var result = await _httpClient.PostAsync($"deliver/{contractId}", requestContent);
        return await result.Content.ReadFromJsonAsync<ApiFailedResponse>();
    }

    public async Task<ApiFailedResponse> ReceiveAsync(int contractId, string accountFrom)
    {
        var body = JsonSerializer.Serialize(new { from = accountFrom });

        _logger.LogInformation($"POST receive/{contractId}; body: {body}");
        
        var requestContent = new StringContent(body, Encoding.UTF8, "application/json");
        
        var result = await _httpClient.PostAsync($"receive/{contractId}", requestContent);
        return await result.Content.ReadFromJsonAsync<ApiFailedResponse>();
    }
    
    public async Task<ApiFailedResponse> EndContractAsync(int contractId, string accountFrom)
    {
        var body = JsonSerializer.Serialize(new { account = accountFrom });

        _logger.LogInformation($"POST end-contract/{contractId}; body: {body}");
        
        var requestContent = new StringContent(body, Encoding.UTF8, "application/json");
        
        var result = await _httpClient.PostAsync($"end-contract/{contractId}", requestContent);
        return await result.Content.ReadFromJsonAsync<ApiFailedResponse>();
    }
}