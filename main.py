import argparse

from models.validator import Validator
from util.pretty_print import pretty_print_players, pretty_print_player_list

from discord_timestamps import format_timestamp, TimestampType
import arrow

# Use the below if you want to run the script w/o using command line arguments
battlefy_csv_filename = ''
gform_csv_filename = ''

# Update these varibles per qualifier for the final print block
END_OF_REGISTRATION_TIMESTAMP = "<t:1729828740:F>"
Q_NUMBER = "#3"

def runner():
    validation = Validator(battlefy_csv_filename, gform_csv_filename)

    print("*The below message was generated on", format_timestamp(arrow.utcnow(), TimestampType.LONG_DATETIME), "via an automatic script*")

    print("\n## Splashtag Errors on Battlefy")

    missing_splashtag_result = validation.get_missing_splashtags_from_battlefy()

    if len(missing_splashtag_result.keys()) == 0:
        print("No Splashtag errors found. Good job everyone!")
    else:
        print("The below teams have improperly formatted Splashtags on Battlefy:")

        sorted_team_names = sorted(missing_splashtag_result.keys())

        for team in sorted_team_names:
            bad_splashtags = pretty_print_players(missing_splashtag_result[team])
            team_captain_discord = validation.battlefy_teams[team].captain.discord
            print(f"- {team}: @{team_captain_discord} |{bad_splashtags}")

    print("\n## Teams that have not registered via Google form")

    teams_not_on_gform = validation.get_teams_not_on_gform()

    if len(teams_not_on_gform) == 0:
        print("No missing Google Form Registrations. Good job everyone!")
    else:
        print("The below teams registered on Battlefy but did not register via Google Form:")

        for team_diff in teams_not_on_gform:
            team_name = team_diff.battlefy.name
            team_captain_discord = validation.battlefy_teams[team_name].captain.discord
            print(f"- `{team_name}`: @{team_captain_discord}")

    print("\n## Splashtag Cross Check")

    splashtag_conflicts = validation.get_splashtag_conflicts()

    if len(splashtag_conflicts) == 0:
        print("No Splashtag conflicts. Good job everyone!")
    else:
        print("The below teams have players with splashtags that are different across Battlefy and Google Form "
              "registrations:")

        for team_name, player_diff in splashtag_conflicts.items():
            only_in_battlefy = pretty_print_player_list(list(player_diff.battlefy))
            only_in_gform = pretty_print_player_list(list(player_diff.gform))
            print(f"- {team_name}: @{validation.battlefy_teams[team_name].captain.discord}")

            if len(only_in_battlefy) > 0:
                print(f"  - Players only on Battlefy:{only_in_battlefy}")
            if len(only_in_gform) > 0:
                print(f"  - Players only on Google Form:{only_in_gform}")

    print("\n**Please note that all registration issues must be resolved by", END_OF_REGISTRATION_TIMESTAMP, ". Any players with missing or incorrect Splashtags after this date will be dropped and cannot play for Qualifier", Q_NUMBER, ". Any teams with less than 4 players or teams that have not registered via Google form will also be dropped.  __This deadline cannot be extended for any reason.__ You will be unable to update player names after", END_OF_REGISTRATION_TIMESTAMP, "Please read the ruleset found in #circuit-info for more information.**")
    print("\nAs a reminder, here are the different ways your team registration may have issues:")
    print("- `Splashtag Errors on Battlefy`")
    print("  - If your team in this section, this means there are player(s) that do not have a valid Splashtag on Battlefy. We do require the full Splashtag, including the pound sign and the 4 or 5 digit number afterwards. For example, `VeronIKA#1234` is a valid Splashtag. `VeronIKA` is not acceptable. For more information, [refer to this guide made by our friends at IPL](<https://docs.google.com/document/d/14oxhAWuwxXqSwE0ZX-LB2wTdFX4BEY08hMLwRqu_O3k/edit#heading=h.jvd3a86dfp7c>).")
    print("- `Teams that have not registered via Google form`")
    print("  - If your team in this section, this means that you have not registered your team using the Google form. All teams are required to fill out the CCA Circuit Google Registration form found in #circuit-info")
    print("- `Splashtag Cross Check`")
    print("  - If your team in this section, this means that there are players that are not on Battlefy or part of your roster originally submitted during Google Registration. Player(s) may be in this section if their Splashtag are different between registrations. Please add or update this player by filling out the Roster Changes Form in #circuit-info")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='SplashtagChecker',
        description='Checks Splashtags given two csvs from Google Forms and Battlefy',
        epilog='Written by dama for the CCA, hi Frosty!')

    parser.add_argument('-b', '--battlefy-filename', help='File path to Battlefy\'s csv export')
    parser.add_argument('-g', '--gform-filename', help='File path to Google Form\'s csv export')
    args = parser.parse_args()

    if args.battlefy_filename is not None:
        battlefy_csv_filename = args.battlefy_filename
    if args.gform_filename is not None:
        gform_csv_filename = args.gform_filename

    runner()
