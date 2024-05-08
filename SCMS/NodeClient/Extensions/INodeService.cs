using NodeClient.Data.Model;

namespace NodeClient.Extensions;

public interface INodeService
{
    Task<IEnumerable<Company>?> GetCompaniesAsync();
    Task<IEnumerable<Contract>?> GetContractsAsync();
    Task<IEnumerable<Inventory>?> GetInventoryAsync();
    Task<IEnumerable<Product>?> GetProductsAsync();
    Task<Tuple<bool, bool>?> GetContractFulfilmentAsync(int contractId);
    Task<IEnumerable<string>?> GetContractTrailAsync(int contractId);
    Task<ContractData?> GetContractDataAsync(int contractId);

    Task<HttpResponseMessage> StartNewContractAsync(Company supplier, Product product, int quatinty, string account);
    Task<HttpResponseMessage> HandoverAsync(int contractId, string accountFrom, string accountTo);
    Task<HttpResponseMessage> ReceiveAsync(int contractId, string accountFrom);
    Task<HttpResponseMessage> EndContractAsync(int contractId, string accountFrom);
}