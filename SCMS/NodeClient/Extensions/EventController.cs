using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;
using NodeClient.Data.Model;
using NodeClient.Extensions;

namespace NodeClient.Extensions;

[Route("/event")]
[ApiController]
public class EventController : ControllerBase
{
    private readonly ILogger _logger;
    private readonly IHubContext<TransferHub, INotificationClient> _hubContext;

    public EventController(ILogger<EventController> logger, IHubContext<TransferHub, INotificationClient> hubContext)
    {
        _logger = logger;
        _hubContext = hubContext;
    }

    [HttpPost]
    public async Task<TransferProductEvent> Post([FromBody] TransferProductEvent transferEvent)
    {
        if (transferEvent == null)
        {
            _logger.LogInformation("Transfer Event is null");
            return null;
        }
        
        _logger.LogInformation($"Event: {transferEvent.Holder} delivers to {transferEvent.NewHolder} for contract {transferEvent.AgreementId}");
        await _hubContext.Clients.All.ReceiveTransferDetails(transferEvent);

        return transferEvent;
    }
}