using Microsoft.AspNetCore.SignalR;
using NodeClient.Extensions;

namespace NodeClient.Components.Services;

public class HandOverNotifier : BackgroundService
{
    private static readonly TimeSpan Period = TimeSpan.FromSeconds(3);
    private readonly ILogger<HandOverNotifier> _logger;
    private readonly IHubContext<TransferHub, INotificationClient> _context;
    private readonly INodeService _nodeService;

    public HandOverNotifier(ILogger<HandOverNotifier> logger, IHubContext<TransferHub, INotificationClient> context, INodeService nodeService)
    {
        _logger = logger;
        _context = context;
        _nodeService = nodeService;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        using var timer = new PeriodicTimer(Period);

        while (!stoppingToken.IsCancellationRequested &&
               await timer.WaitForNextTickAsync(stoppingToken))
        {
            var dateTime = DateTime.Now;
            _logger.LogInformation("Requesting blockchain's emitted events");
            await _nodeService.GetEvents();
        }
    }
}