using Microsoft.AspNetCore.SignalR;
using NodeClient.Data.Model;

namespace NodeClient.Extensions;

public class TransferHub : Hub<INotificationClient>
{
}

public interface INotificationClient
{
    Task ReceiveTransferDetails(TransferProductEvent eventData);
}