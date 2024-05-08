using Microsoft.AspNetCore.Identity;

namespace NodeClient.Data;

// Add profile data for application users by adding properties to the ApplicationUser class
public class ApplicationUser : IdentityUser
{
    public string Account { get; set; }
}