
from SimpleAgent.litellm_interface import LitellmInterface

# Example Code
code = """
/// <summary>
/// Represents a user with a first name, last name, and username.
/// </summary>
public class User
{
    /// <summary>
    /// Gets or sets the user's first name.
    /// </summary>
    public string FirstName { get; set; }

    /// <summary>
    /// Gets or sets the user's last name.
    /// </summary>
    public string LastName { get; set; }

    /// <summary>
    /// Gets or sets the user's username.
    /// </summary>
    public string Username { get; set; }

    /// <summary>
    /// Gets or sets the user's email address.
    /// </summary>
    public string Email { get; set; }

    /// <summary>
    /// Gets or sets the user's phone number.
    /// </summary>
    public string PhoneNumber { get; set; }

    /// <summary>
    /// Gets or sets the user's date of birth.
    /// </summary>
    public DateTime DateOfBirth { get; set; }

    /// <summary>
    /// Gets or sets the user's address.
    /// </summary>
    public string Address { get; set; }

    /// <summary>
    /// Gets or sets the user's city.
    /// </summary>
    public string City { get; set; }

    /// <summary>
    /// Gets or sets the user's state or province.
    /// </summary>
    public string State { get; set; }

    /// <summary>
    /// Gets or sets the user's postal code.
    /// </summary>
    public string PostalCode { get; set; }

    /// <summary>
    /// Gets or sets the user's country.
    /// </summary>
    public string Country { get; set; }

    /// <summary>
    /// Gets or sets the user's profile picture URL.
    /// </summary>
    public string ProfilePictureUrl { get; set; }

    /// <summary>
    /// Gets or sets the date when the user registered.
    /// </summary>
    public DateTime RegistrationDate { get; set; }

    /// <summary>
    /// Gets or sets the user's last login date.
    /// </summary>
    public DateTime LastLoginDate { get; set; }

    /// <summary>
    /// Gets or sets whether the user's email is verified.
    /// </summary>
    public bool IsEmailVerified { get; set; }

    /// <summary>
    /// Gets or sets whether the user's account is active.
    /// </summary>
    public bool IsActive { get; set; }

    /// <summary>
    /// Gets or sets the user's role in the system.
    /// </summary>
    public string Role { get; set; }

    /// <summary>
    /// Gets or sets the user's preferences.
    /// </summary>
    public UserPreferences Preferences { get; set; }

    /// <summary>
    /// Gets or sets the user's security questions.
    /// </summary>
    public List<SecurityQuestion> SecurityQuestions { get; set; }

    /// <summary>
    /// Gets or sets the user's payment methods.
    /// </summary>
    public List<PaymentMethod> PaymentMethods { get; set; }

    /// <summary>
    /// Gets or sets the user's order history.
    /// </summary>
    public List<Order> OrderHistory { get; set; }

    /// <summary>
    /// Gets or sets the user's wishlist.
    /// </summary>
    public List<Product> Wishlist { get; set; }

    /// <summary>
    /// Gets or sets the user's cart.
    /// </summary>
    public Cart ShoppingCart { get; set; }

    /// <summary>
    /// Gets or sets the user's notification settings.
    /// </summary>
    public NotificationSettings NotificationSettings { get; set; }

    /// <summary>
    /// Gets or sets the user's subscription status.
    /// </summary>
    public SubscriptionStatus SubscriptionStatus { get; set; }

    /// <summary>
    /// Gets or sets the user's loyalty points.
    /// </summary>
    public int LoyaltyPoints { get; set; }

    /// <summary>
    /// Gets or sets the user's referral code.
    /// </summary>
    public string ReferralCode { get; set; }

    /// <summary>
    /// Gets or sets the users who were referred by this user.
    /// </summary>
    public List<User> Referrals { get; set; }

    /// <summary>
    /// Gets or sets the user's social media profiles.
    /// </summary>
    public SocialMediaProfiles SocialMediaProfiles { get; set; }

    /// <summary>
    /// Gets or sets the user's device information.
    /// </summary>
    public List<DeviceInfo> Devices { get; set; }

    /// <summary>
    /// Gets or sets the user's login history.
    /// </summary>
    public List<LoginRecord> LoginHistory { get; set; }

    /// <summary>
    /// Gets or sets the user's activity log.
    /// </summary>
    public List<ActivityLogEntry> ActivityLog { get; set; }

    /// <summary>
    /// Gets or sets the user's saved addresses.
    /// </summary>
    public List<Address> SavedAddresses { get; set; }

    /// <summary>
    /// Gets or sets the user's communication preferences.
    /// </summary>
    public CommunicationPreferences CommunicationPreferences { get; set; }

    /// <summary>
    /// Gets or sets the user's privacy settings.
    /// </summary>
    public PrivacySettings PrivacySettings { get; set; }

    /// <summary>
    /// Gets or sets the user's two-factor authentication settings.
    /// </summary>
    public TwoFactorAuthSettings TwoFactorAuthSettings { get; set; }

    /// <summary>
    /// Gets or sets the user's language preference.
    /// </summary>
    public string PreferredLanguage { get; set; }

    /// <summary>
    /// Gets or sets the user's timezone.
    /// </summary>
    public string Timezone { get; set; }

    /// <summary>
    /// Gets or sets the user's currency preference.
    /// </summary>
    public string PreferredCurrency { get; set; }

    /// <summary>
    /// Gets or sets the user's reviews.
    /// </summary>
    public List<Review> Reviews { get; set; }

    /// <summary>
    /// Gets or sets the user's comments.
    /// </summary>
    public List<Comment> Comments { get; set; }

    /// <summary>
    /// Gets or sets the user's followed topics.
    /// </summary>
    public List<Topic> FollowedTopics { get; set; }

    /// <summary>
    /// Gets or sets the user's followed users.
    /// </summary>
    public List<User> FollowedUsers { get; set; }

    /// <summary>
    /// Gets or sets the users following this user.
    /// </summary>
    public List<User> Followers { get; set; }

    /// <summary>
    /// Gets or sets the user's blocked users.
    /// </summary>
    public List<User> BlockedUsers { get; set; }

    /// <summary>
    /// Gets or sets the user's achievements.
    /// </summary>
    public List<Achievement> Achievements { get; set; }

    /// <summary>
    /// Gets or sets the user's badges.
    /// </summary>
    public List<Badge> Badges { get; set; }

    /// <summary>
    /// Gets or sets the user's skills.
    /// </summary>
    public List<Skill> Skills { get; set; }

    /// <summary>
    /// Gets or sets the user's education history.
    /// </summary>
    public List<Education> EducationHistory { get; set; }

    /// <summary>
    /// Gets or sets the user's work experience.
    /// </summary>
    public List<WorkExperience> WorkExperience { get; set; }

    /// <summary>
    /// Gets or sets the user's certifications.
    /// </summary>
    public List<Certification> Certifications { get; set; }

    /// <summary>
    /// Gets or sets the user's projects.
    /// </summary>
    public List<Project> Projects { get; set; }

    /// <summary>
    /// Gets or sets the user's publications.
    /// </summary>
    public List<Publication> Publications { get; set; }

    /// <summary>
    /// Gets or sets the user's patents.
    /// </summary>
    public List<Patent> Patents { get; set; }

    /// <summary>
    /// Gets or sets the user's courses.
    /// </summary>
    public List<Course> Courses { get; set; }

    /// <summary>
    /// Gets or sets the user's volunteer experience.
    /// </summary>
    public List<VolunteerExperience> VolunteerExperience { get; set; }

    /// <summary>
    /// Gets or sets the user's languages.
    /// </summary>
    public List<Language> Languages { get; set; }

    /// <summary>
    /// Gets or sets the user's interests.
    /// </summary>
    public List<Interest> Interests { get; set; }
}
"""

system_message = "You help edit code. You will be given a code file, and a snippet as well as instructions for how to implement the snippet in the provided code. Return only the final code file with the snippet implemented."

# model = "anthropic/claude-3-5-haiku-latest"
model = "openai/gpt-4o-mini"

bot = LitellmInterface(
    name="code_predictor",
    model=model,
    system_role=system_message,
    stream=True,
)

# Get response from the AI
print("\nAssistant: ", end="", flush=True)

response = bot.prompt(prompt=f"Replace the Username property with an Email property. Respond only with code, and with no markdown formatting.{code}", predicted_output=code)

for chunk in response:
    print(chunk, end="", flush=True)
print("\n")