using NodeClient.Data.Model;

namespace NodeClient.Extensions;

public interface INodeService
{
    Task<IEnumerable<Company>?> GetCompaniesAsync();
    Task<IEnumerable<Contract>?> GetContractsAsync();
    Task<IEnumerable<Inventory>?> GetInventoryAsync();
    Task<IEnumerable<Product>?> GetProductsAsync();
    Task<Fulfilment?> GetContractFulfilmentAsync(int contractId);
    Task<IEnumerable<Company>?> GetContractTrailAsync(int contractId);
    Task<ContractData?> GetContractDataAsync(int contractId);
    Task GetEvents();
    Task<ApiFailedResponse> StartNewContractAsync(Company supplier, Product product, int quatinty, string account);
    Task<ApiFailedResponse> HandoverAsync(int contractId, string accountFrom, string accountTo);
    Task<ApiFailedResponse> ReceiveAsync(int contractId, string accountFrom);
    Task<ApiFailedResponse> EndContractAsync(int contractId, string accountFrom);
}