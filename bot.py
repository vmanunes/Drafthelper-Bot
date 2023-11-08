from __future__ import print_function
import discord
import math
import random
import asyncio
from discord import app_commands
from discord.enums import ChannelType
from googleapiclient.discovery import build 
from google.oauth2 import service_account
from dotenv import dotenv_values

SCOPES = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = service_account.Credentials.from_service_account_file('google-credentials.json', scopes=SCOPES)
spreadsheet_service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

config = dotenv_values()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Functions for swiss bracketmaker
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def edit_cell (sheetId,cellRow,cellColumn,newValue,requestList,numerical):
    if numerical == True:
        requestList.append({
            "updateCells": {
                "range": {
                    "endRowIndex": cellRow+1, # The end row (exclusive) of the range, or not set if unbounded.
                    "endColumnIndex": cellColumn+1, # The end column (exclusive) of the range, or not set if unbounded.
                    "sheetId": sheetId, # The sheet this range is on.
                    "startColumnIndex": cellColumn, # The start column (inclusive) of the range, or not set if unbounded.
                    "startRowIndex": cellRow, # The start row (inclusive) of the range, or not set if unbounded.
                },
                "rows": [
                    {
                        "values": {
                            "userEnteredValue": {
                                "numberValue": newValue
                            }
                        }
                    }
                ],
                "fields": "userEnteredValue/numberValue",
                }
        })
    else:
        requestList.append({
            "updateCells": {
                "range": {
                    "endRowIndex": cellRow+1, # The end row (exclusive) of the range, or not set if unbounded.
                    "endColumnIndex": cellColumn+1, # The end column (exclusive) of the range, or not set if unbounded.
                    "sheetId": sheetId, # The sheet this range is on.
                    "startColumnIndex": cellColumn, # The start column (inclusive) of the range, or not set if unbounded.
                    "startRowIndex": cellRow, # The start row (inclusive) of the range, or not set if unbounded.
                },
                "rows": [
                    {
                        "values": {
                            "userEnteredValue": {
                                "stringValue": str(newValue)
                            }
                        }
                    }
                ],
                "fields": "userEnteredValue/stringValue",
                }
        })

def first_empty_cell (spreadsheetId,page,column):
    count = 0
    for row in spreadsheetId['sheets'][page]['data'][0]['rowData']:
        if 'formattedValue' in row['values'][column].keys():
            count += 1
    return count

def create_matchup (player1name,player1id,player2name,player2id,rowNumber,rowOffset,roundNumber,request,dataSheetId,matchupSheetId,player1loss,player2loss):
    edit_cell(matchupSheetId,(rowNumber+rowOffset),1,roundNumber,request,True)
    edit_cell(matchupSheetId,(rowNumber+rowOffset),2,player1name,request,False)
    edit_cell(matchupSheetId,(rowNumber+rowOffset),3,player2name,request,False)
    edit_cell(matchupSheetId,(rowNumber+rowOffset),4,player1loss,request,False)
    edit_cell(matchupSheetId,(rowNumber+rowOffset),5,player2loss,request,False)
    if player2name != 'BYE' and player2id != '-':
        edit_cell(dataSheetId,(int(player1id)),(int(roundNumber)+8),player2id,request,True)
        edit_cell(dataSheetId,(int(player2id)),(int(roundNumber)+8),player1id,request,True)

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# End of functions
# --------------------------------------------------------------------------------------------------     
# -------------------------------------------------------------------------------------------------- 

# global variables
toggleRoleMessages = False
# trackers to check if public commands have been called recently, there's probably a better way to do this
resourcesCd = False
templateCd = False
sampleCd = False
circuitCd = False
pingCd = False
helpCd = False
scheduleCd = False
nextMatchCd = False

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: discord.Message):
    rolecheck = False
    global toggleRoleMessages
    if message.author == client.user:
        return
    for role in message.author.roles:
        # UPDATE LATER WITH FLEXIBLE ADMIN ROLES FOR EACH SERVER
        if role.permissions.administrator:
            rolecheck = True
        if role.name in 'Tournament Staff':
            rolecheck = True

    # --------------------------------------------------------------------------------------------------
    # General use commands
    # --------------------------------------------------------------------------------------------------

    # ping
    if message.content.startswith('s!ping'):
        global pingCd
        if pingCd == False:
            await message.reply('Pong.')
            pingCd = True
            await asyncio.sleep(5)
            pingCd = False
        else:
            if rolecheck == True:
                await message.reply('Pong.')

    # Resources
    if message.content.startswith('s!resources'):
        global resourcesCd
        if resourcesCd == False:
            await message.reply('You can find resources that will help introduce you to the Draft format, or run your own league, on the following thread: https://www.smogon.com/forums/threads/draft-league-resources.3716128/')
            resourcesCd = True
            await asyncio.sleep(60)
            resourcesCd = False
        else:
            if rolecheck == True:
                await message.reply('You can find resources that will help introduce you to the Draft format, or run your own league, on the following thread: https://www.smogon.com/forums/threads/draft-league-resources.3716128/')

    # Template
    if message.content.startswith('s!template'):
        global templateCd
        if templateCd == False:
            await message.reply('<https://spo.ink/draft_league_16_coach_template>')
            templateCd = True
            await asyncio.sleep(60)
            templateCd = False
        else:
            if rolecheck == True:
                await message.reply('<https://spo.ink/draft_league_16_coach_template>')
    
    # Tiers
    if message.content.startswith('s!sample'):
        global sampleCd
        if sampleCd == False:
            await message.reply('The sample draft boards are currently being updated to account for the DLC release and will be available later.')
            sampleCd = True
            await asyncio.sleep(60)
            sampleCd = False
        else:
            if rolecheck == True:
                await message.reply('The sample draft boards are currently being updated to account for the DLC release and will be available later.')
    
    # Circuit
    if message.content.startswith('s!circuit'):
        global circuitCd
        if circuitCd == False:
            await message.reply("All information regarding this year's circuit can be found at <https://www.smogon.com/forums/threads/calendar.3713506/> and the current circuit standings can be found on this spreadsheet <https://spo.ink/draft_league_circuit_2023>.")
            circuitCd = True
            await asyncio.sleep(60)
            circuitCd = False
        else:
            if rolecheck == True:
                await message.reply("All information regarding this year's circuit can be found at <https://www.smogon.com/forums/threads/calendar.3713506/> and the current circuit standings can be found on this spreadsheet <https://spo.ink/draft_league_circuit_2023>.")

    # DCL Schedule
    if message.content.startswith('s!schedule'):
        global scheduleCd
        if scheduleCd == False:
            spreadsheet = spreadsheet_service.spreadsheets().get(spreadsheetId='1oDzkyszf12fSlG8LtRdsNNTowWTcgpjo36FuP9dAI3k',includeGridData=True, ranges='Bot!C:C').execute()
            if 'formattedValue' in spreadsheet['sheets'][0]['data'][0]['rowData'][1]['values'][0].keys():
                    scheduleMessage = spreadsheet['sheets'][0]['data'][0]['rowData'][1]['values'][0]
                    await message.channel.send(scheduleMessage['formattedValue'])
                    scheduleCd = True
                    await asyncio.sleep(60)
                    scheduleCd = False
        else:
            if rolecheck == True:
                spreadsheet = spreadsheet_service.spreadsheets().get(spreadsheetId='1oDzkyszf12fSlG8LtRdsNNTowWTcgpjo36FuP9dAI3k',includeGridData=True, ranges='Bot!C:C').execute()
                if 'formattedValue' in spreadsheet['sheets'][0]['data'][0]['rowData'][1]['values'][0].keys():
                        scheduleMessage = spreadsheet['sheets'][0]['data'][0]['rowData'][1]['values'][0]
                        await message.channel.send(scheduleMessage['formattedValue'])

    # DCL next match
    if message.content.startswith('s!next'):
        global nextMatchCd
        if nextMatchCd == False:
            spreadsheet = spreadsheet_service.spreadsheets().get(spreadsheetId='1oDzkyszf12fSlG8LtRdsNNTowWTcgpjo36FuP9dAI3k',includeGridData=True, ranges='Bot!C:C').execute()
            if 'formattedValue' in spreadsheet['sheets'][0]['data'][0]['rowData'][2]['values'][0].keys():
                    nextMatchMessage = spreadsheet['sheets'][0]['data'][0]['rowData'][2]['values'][0]
                    await message.channel.send(nextMatchMessage['formattedValue'])
                    nextMatchCd = True
                    await asyncio.sleep(60)
                    nextMatchCd = False
        else:
            if rolecheck == True:
                spreadsheet = spreadsheet_service.spreadsheets().get(spreadsheetId='1oDzkyszf12fSlG8LtRdsNNTowWTcgpjo36FuP9dAI3k',includeGridData=True, ranges='Bot!C:C').execute()
                if 'formattedValue' in spreadsheet['sheets'][0]['data'][0]['rowData'][2]['values'][0].keys():
                        nextMatchMessage = spreadsheet['sheets'][0]['data'][0]['rowData'][2]['values'][0]
                        await message.channel.send(nextMatchMessage['formattedValue'])
            
    # Help
    if message.content.startswith('s!help'):
        global helpCd
        if helpCd == False:
            embed = discord.Embed(title='DraftHelper Commands')
            embed.add_field(name='s!resources',value='Links to the resources thread on the Smogon forums.', inline=False)
            embed.add_field(name='s!template',value='Links to a 16 coach draft template sheet.', inline=False)
            embed.add_field(name='s!sample',value='Links to sample draft boards for various different draft formats.', inline=False)
            embed.add_field(name='s!circuit',value="Links to the subforum's calendar thread on the Smogon forums and to the circuit spreadsheet.", inline=False)
            await message.channel.send(embed=embed)
            helpCd = True
            await asyncio.sleep(5)
            helpCd = False
        else:
            if rolecheck == True:
                embed = discord.Embed(title='DraftHelper Commands')
                embed.add_field(name='s!resources',value='Links to the resources thread on the Smogon forums.', inline=False)
                embed.add_field(name='s!template',value='Links to a 16 coach draft template sheet.', inline=False)
                embed.add_field(name='s!sample',value='Links to sample draft boards for various different draft formats.', inline=False)
                embed.add_field(name='s!circuit',value="Links to the subforum's calendar thread on the Smogon forums and to the circuit spreadsheet.", inline=False)
                await message.channel.send(embed=embed)


    # --------------------------------------------------------------------------------------------------
    # Admin commands
    # --------------------------------------------------------------------------------------------------

    # Admin commands Help
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------   
    if message.content.startswith('s!adminHelp'):
        if rolecheck == False:
            await message.channel.send('You do not have the required permissions to run this command!')
            return
        embed = discord.Embed(title='DraftHelper Admin Commands')
        embed.add_field(name='s!assignDraftPools [ID] (Competitor role)',value='Assign pools on column A to users in column B in the "Draft Pools" tab on the given google spreadsheet. Competitor role is optional and will be added alongside draft pool role.', inline=False)
        embed.add_field(name='s!removeDraftPools',value='Remove all Draft Pool roles from users in this server.', inline=False)
        embed.add_field(name='s!assignBattlePools [ID]',value='Assign pools on column A to users in column B in the "Battle Pools" tab on the given google spreadsheet. Pool roles are configured to be groups of 8 pools (i.e. Battle Pools 1-8).', inline=False)
        embed.add_field(name='s!removeBattlePools',value='Remove all Battle Pool roles from users in this server.', inline=False)
        embed.add_field(name='s!setupDraftChannels [ID]',value='Sends the opening messages on each draft pool channel and creates the discussion threads. Messages should be on column A in the "Channel Messages" tab on the given google spreadsheet.', inline=False)
        embed.add_field(name='s!resetDraftChannels',value='Looks for channels that are named X-draft-done and removes the "-done".', inline=False)
        embed.add_field(name='s!toggleMessages [on/off]',value='Toggles whether or not the bot will send confirmation messages for each role that is added / removed (default off).', inline=False)
        embed.add_field(name='s!verifyUsers [ID]',value='Checks if any user in the list in the "Not Verified" tab in the doc is verified in the server or not.', inline=False)
        embed.add_field(name='s!removeCompetitorRoles',value='Removes the competitor roles for the current circuit. NOTE: This command is currently hardcoded to only work with a specific role, and is in the process of being updated.', inline=False)
        embed.add_field(name='s!updateSwissBracket [ID]',value='Runs the swiss bracketmaker tool. Requires a sheet properly configured to run with it. Contact @vmnunes for more information.', inline=False)
        await message.channel.send(embed=embed)

    # Assign Draft Pools
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
    if message.content.startswith("s!assignDraftPools"):
        if rolecheck == False:
            await message.channel.send('You do not have the required permissions to run this command!')
            return
        message_args = message.content.split(' ', 2)[1:]
        if len(message_args) == 0:
            await message.channel.send('This command requires 1 argument (i.e. !assignDraftPools [ID])')
        else:
            await message.channel.send('Assigning draft pool roles. This might take some time.')
            thisGuild = client.get_guild(message.guild.id)
            spreadsheet = spreadsheet_service.spreadsheets().get(spreadsheetId=message_args[0],includeGridData=True, ranges='Draft Pools!A:B').execute()
            for row in spreadsheet['sheets'][0]['data'][0]['rowData']:
                if 'formattedValue' in row['values'][0].keys() or 'formattedValue' in row['values'][1].keys():
                    exists = False
                    competitor_role_exists = False
                    memberName = row['values'][1]
                    pool = row['values'][0]
                    newrole = 'Draft Pool {}'.format(pool['formattedValue'])
                    new_role = None
                    competitor_role = None
                    member = thisGuild.get_member_named(memberName['effectiveValue']['stringValue'])
                    if member != None:
                        for role in await thisGuild.fetch_roles():
                            if role.name == newrole:
                                exists = True
                                new_role = role
                            if len(message_args) == 2:
                                if role.name == message_args[1]:
                                    competitor_role_exists = True
                                    competitor_role = role
                        if exists == False:
                            new_role = await thisGuild.create_role(name=newrole)
                        if len(message_args) == 2:
                            if competitor_role_exists == False:
                                competitor_role = await thisGuild.create_role(name=message_args[1])
                        
                        if member.get_role(new_role.id) == None:
                            await member.add_roles(new_role, reason="Tournament automation sorting")
                            if toggleRoleMessages:
                                await message.channel.send('Adding pool {} to member {}'.format(pool['formattedValue'], member.display_name))
                        else:
                            if toggleRoleMessages:
                                await message.channel.send('User {} already in the pool #{}'.format(member.display_name, pool['formattedValue']))
                        if len(message_args) == 2:
                            if member.get_role(competitor_role.id) == None:
                                await member.add_roles(competitor_role, reason="Tournament automation sorting")
                    else:
                        await message.channel.send('**{}: User {} from Draft Pool {} was not found in this server**'.format(f'{message.author.mention}', memberName['effectiveValue']['stringValue'], pool['formattedValue']))
            await message.channel.send('**{}: All draft pool roles have been added.**'.format(f'{message.author.mention}'))

    # Remove Draft Pools
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------        
    if message.content.startswith("s!removeDraftPools"):
        if rolecheck == False:
            await message.channel.send('You do not have the required permissions to run this command!')
            return
        await message.channel.send('Removing draft pool roles. This might take some time.')
        thisGuild = client.get_guild(message.guild.id)
        for role in thisGuild.roles:
            if 'Draft Pool' in role.name:
                for member in role.members:
                    await member.remove_roles(role)
                    if toggleRoleMessages:
                        await message.channel.send('Removing pool {} from member {}'.format(role.name, member.display_name))
        await message.channel.send('**{}: All draft pool roles have been removed.**'.format(f'{message.author.mention}'))

    # Toggle Messages
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------   
    if message.content.startswith("s!toggleMessages"):
        if rolecheck == False:
            await message.channel.send('You do not have the required permissions to run this command!')
            return
        message_args = message.content.split(' ')[1:]
        if len(message_args) == 0:
            await message.channel.send('This command requires 1 argument (i.e. s!toggleMessages [on/off])')
        else:
            if message_args[0] == 'on':
                toggleRoleMessages = True
                await message.channel.send('Bot will send messages for each assigned or removed role.')
            if message_args[0] == 'off':
                toggleRoleMessages = False
                await message.channel.send('Bot will no longer send messages for each assigned or removed role.')
            if message_args[0] != 'on' and message_args[0] != 'off':
                await message.channel.send('Invalid argument! (must be "on" or "off")')

    # Remove Battle Pools
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------   
    if message.content.startswith("s!removeBattlePools"):
        if rolecheck == False:
            await message.channel.send('You do not have the required permissions to run this command!')
            return
        await message.channel.send('Removing battle pool roles. This might take some time.')
        thisGuild = client.get_guild(message.guild.id)
        for role in thisGuild.roles:
            if 'Battle Pools' in role.name:
                for member in role.members:
                    await member.remove_roles(role)
                    if toggleRoleMessages:
                        await message.channel.send('Removing {} from member {}'.format(role.name, member.display_name))
        await message.channel.send('**{}: All battle pool roles have been removed.**'.format(f'{message.author.mention}'))

    # Assign Battle Pools
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------   
    if message.content.startswith("s!assignBattlePools"):
        if rolecheck == False:
            await message.channel.send('You do not have the required permissions to run this command!')
            return
        message_args = message.content.split(' ')[1:]
        if len(message_args) == 0:
            await message.channel.send('This command requires 1 argument (i.e. !assignBattlePools [ID])')
        else:
            await message.channel.send('Assigning battle pool roles. This might take some time.')
            thisGuild = client.get_guild(message.guild.id)
            spreadsheet = spreadsheet_service.spreadsheets().get(spreadsheetId=message_args[0],includeGridData=True, ranges='Battle Pools!A:B').execute()
            for row in spreadsheet['sheets'][0]['data'][0]['rowData']:
                if 'formattedValue' in row['values'][0].keys() or 'formattedValue' in row['values'][1].keys():
                    exists = False
                    competitor_role_exists = False
                    memberName = row['values'][1]
                    pool = row['values'][0]
                    poolRangeLower = str((((math.ceil(int(pool['formattedValue'])/8))-1)*8)+1)
                    poolRangeHigher = str((((math.ceil(int(pool['formattedValue'])/8))-1)*8)+8)
                    newrole = 'Battle Pools {}-{}'.format(poolRangeLower, poolRangeHigher)
                    new_role = None
                    competitor_role = None
                    member = thisGuild.get_member_named(memberName['effectiveValue']['stringValue'])
                    if member != None:
                        for role in await thisGuild.fetch_roles():
                            if role.name == newrole:
                                exists = True
                                new_role = role
                        if exists == False:
                            new_role = await thisGuild.create_role(name=newrole)                        
                        if member.get_role(new_role.id) == None:
                            await member.add_roles(new_role, reason="Tournament automation sorting")
                            if toggleRoleMessages:
                                await message.channel.send('Adding {} to member {}'.format(newrole, member.display_name))
                        else:
                            if toggleRoleMessages:
                                await message.channel.send('User {} already in a battle pool'.format(member.display_name))
                    else:
                        await message.channel.send('**{}: User {} was not found in this server**'.format(f'{message.author.mention}',memberName['effectiveValue']['stringValue']))
            await message.channel.send('**{}: All battle pool roles have been added.**'.format(f'{message.author.mention}'))
    
    # Reset Draft Channels
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------   
    if message.content.startswith("s!resetDraftChannels"):
        if rolecheck == False:
            await message.channel.send('You do not have the required permissions to run this command!')
            return
        await message.channel.send('Resetting draft channel names.')
        thisGuild = client.get_guild(message.guild.id)
        for channel in thisGuild.text_channels:
            if 'draft-done' in channel.name:
                splitName = channel.name.split('-')
                newName = '{}-{}'.format(splitName[0],splitName[1])
                await channel.edit(name=newName)
        await message.channel.send('**{}: All channel names have been reset.**'.format(f'{message.author.mention}'))

    # Send Channel Messages
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------    
    if message.content.startswith("s!setupDraftChannels"):
        if rolecheck == False:
            await message.channel.send('You do not have the required permissions to run this command!')
            return
        message_args = message.content.split(' ')[1:]
        if len(message_args) == 0:
            await message.channel.send('This command requires 1 argument (i.e. s!setupDraftChannels [ID])')
        else:
            await message.channel.send('Sending messages to all draft channels and creating the discussion threads. This might take some time.')
            thisGuild = client.get_guild(message.guild.id)
            spreadsheet = spreadsheet_service.spreadsheets().get(spreadsheetId=message_args[0],includeGridData=True, ranges='Channel Messages!A:A').execute()
            for index,row in enumerate(spreadsheet['sheets'][0]['data'][0]['rowData']):
                if 'formattedValue' in row['values'][0].keys():
                    channelMessage = row['values'][0]
                    channelTemp = discord.utils.get(thisGuild.channels, name='{}-draft'.format(index+1))
                    currentChannel = client.get_channel(channelTemp.id)
                    sentMessage = await currentChannel.send(channelMessage['formattedValue'])
                    await sentMessage.pin()
                    currentThread = await currentChannel.create_thread(
                        name='Pool Discussion',
                        type=ChannelType.public_thread
                    )
                    await currentThread.send('Please use this thread for general discussions related to the draft pool.')
            await message.channel.send('**{}: All draft pool channels have been setup.**'.format(f'{message.author.mention}'))

    # Check for Verified users
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------  
    if message.content.startswith("s!verifyUsers"):
        if rolecheck == False:
            await message.channel.send('You do not have the required permissions to run this command!')
            return
        message_args = message.content.split(' ')[1:]
        if len(message_args) == 0:
            await message.channel.send('This command requires 1 argument (i.e. s!verify [ID])')
        else:
            await message.channel.send('Checking for non-verified users.')
            thisGuild = client.get_guild(message.guild.id)
            spreadsheet = spreadsheet_service.spreadsheets().get(spreadsheetId=message_args[0],includeGridData=True, ranges='Not Verified!A:A').execute()
            for row in spreadsheet['sheets'][0]['data'][0]['rowData']:
                if 'formattedValue' in row['values'][0].keys():
                    memberName = row['values'][0]
                    member = thisGuild.get_member_named(memberName['effectiveValue']['stringValue'])
                    if member != None:
                        # debug check
                        # await message.channel.send('Checking user {}'.format(member.display_name))
                        # debug check end
                        for role in member.roles:
                            if role.name in 'Not Verified':
                                await message.channel.send('***!!! User {} is not verified !!!***'.format(member.display_name))
                                # await message.channel.send('{}'.format(member.display_name))
                    else:
                        if toggleRoleMessages:
                            await message.channel.send('**{}: User {} was not found in this server**'.format(f'{message.author.mention}',memberName['effectiveValue']['stringValue']))
            await message.channel.send('**{}: Verification complete.**'.format(f'{message.author.mention}'))
    
    
    if message.content.startswith("s!removeCompetitorRoles"):
        if rolecheck == False:
            await message.channel.send('You do not have the required permissions to run this command!')
            return
        await message.channel.send('Removing competitor roles. This might take some time.')
        thisGuild = client.get_guild(message.guild.id)
        # UPDATE THIS WITH A PARAMETER LATER
        for role in thisGuild.roles:
            if 'Summer Seasonal Competitor' in role.name:
                for member in role.members:
                    # await message.channel.send('Removing {} from member {}'.format(role.name, member.display_name))
                    await member.remove_roles(role)
                    if toggleRoleMessages:
                        await message.channel.send('Removing {} from member {}'.format(role.name, member.display_name))
        await message.channel.send('**{}: All competitor roles have been removed.**'.format(f'{message.author.mention}'))

# -------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ SWISS BRACKETMAKER -----------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------

    if message.content.startswith("s!updateSwissBracket"):
        if rolecheck == False:
            await message.channel.send('You do not have the required permissions to run this command!')
            return
        message_args = message.content.split(' ')[1:]
        if len(message_args) == 0:
            await message.channel.send('This command requires 1 argument (i.e. s!updateSwissBracket [ID])')
        else:
            # get sheets
            # dataSpreadsheet = spreadsheet_service.spreadsheets().get(spreadsheetId=message_args[0],includeGridData=True, ranges='Data!A:AL').execute()
            dataSpreadsheet = spreadsheet_service.spreadsheets().get(spreadsheetId=message_args[0],includeGridData=True, ranges=['Data!A:AL','Match History!A:G']).execute()
            dataId = dataSpreadsheet['sheets'][0]['properties']['sheetId'] # get ID of data spreadsheet in the google doc
            matchupId = dataSpreadsheet['sheets'][1]['properties']['sheetId'] # get ID of matchup spreadsheet in the google doc
            lossesCutoff = dataSpreadsheet['sheets'][0]['data'][0]['rowData'][7]['values'][1]['effectiveValue']['numberValue'] # get number of losses for which players are eliminated
            winsCutoff = dataSpreadsheet['sheets'][0]['data'][0]['rowData'][10]['values'][1]['effectiveValue']['numberValue'] # get number of wins for which players are no longer put into matchmaking

            # update round number
            roundNumber = dataSpreadsheet['sheets'][0]['data'][0]['rowData'][1]['values'][1]['effectiveValue']['numberValue'] # get round number
            updatedRoundNumber = roundNumber + 1
            updateRequests = [] # initialize list of sheet update requests
            updateRequests.append({ #create round number update request
                "updateCells": {
                    "range": {
                        "endRowIndex": 2, # The end row (exclusive) of the range, or not set if unbounded.
                        "endColumnIndex": 2, # The end column (exclusive) of the range, or not set if unbounded.
                        "sheetId": dataId, # The sheet this range is on.
                        "startColumnIndex": 1, # The start column (inclusive) of the range, or not set if unbounded.
                        "startRowIndex": 1, # The start row (inclusive) of the range, or not set if unbounded.
                    },
                    "rows": [
                        {
                            "values": {
                                "userEnteredValue": {
                                    "numberValue": updatedRoundNumber
                                }
                            }
                        }
                    ],
                    "fields": "userEnteredValue/numberValue",
                }
            })
            
            # check duplicate player entries
            if dataSpreadsheet['sheets'][0]['data'][0]['rowData'][4]['values'][1]['formattedValue'] == 'ERROR':
                await message.channel.send('{} There are duplicate player entries in the player list! Bracket will not generate!'.format(f'{message.author.mention}')) #output an error if a duplicate player is found
            else:
                await message.channel.send('Creating swiss bracket for round {}.'.format(updatedRoundNumber)) #start bracket generation otherwise

                # create player list based on standings
                playerList = [] 
                for index, row in enumerate(dataSpreadsheet['sheets'][0]['data'][0]['rowData']): 
                    if 'formattedValue' in row['values'][32].keys():
                        if index != 0:
                            sLname = dataSpreadsheet['sheets'][0]['data'][0]['rowData'][index]['values'][32]['formattedValue'] # get player name
                            sLgp = dataSpreadsheet['sheets'][0]['data'][0]['rowData'][index]['values'][33]['formattedValue'] # get player games played
                            sLwins = dataSpreadsheet['sheets'][0]['data'][0]['rowData'][index]['values'][34]['formattedValue'] # get player wins
                            sLres = dataSpreadsheet['sheets'][0]['data'][0]['rowData'][index]['values'][36]['formattedValue'] # get player resistance
                            sLuid = dataSpreadsheet['sheets'][0]['data'][0]['rowData'][index]['values'][37]['formattedValue'] # get player uid
                            sLlosses = dataSpreadsheet['sheets'][0]['data'][0]['rowData'][index]['values'][35]['formattedValue'] # get player losses
                            subList = [sLname, sLgp, sLwins, sLres, sLuid, sLlosses] # create sublist with player data
                            playerList.append(subList) # add sublist to the player list

                # remove drops and eliminated players from player list
                playersToRemove = []
                for i in range(0,len(playerList)):
                    numcheck = (str(playerList[i][0]))[4:] # numerical character check for checking drops
                    if (str(playerList[i][0]).startswith('Drop') and len(playerList[i][0]) <= 6 and numcheck.isnumeric()) or int(playerList[i][5]) >= lossesCutoff or (int(playerList[i][2]) >= winsCutoff and winsCutoff != 0):
                        playersToRemove.append(i)
                for index in sorted(playersToRemove, reverse = True):
                    del playerList[index]

                # check if odd number of players
                oddRound = False
                if not (len(playerList) % 2 == 0):
                    await message.channel.send('{} There is an odd number of players in the bracket. One player will receive a bye.'.format(f'{message.author.mention}'))
                    oddRound = True

                count = 0
                # check if round > 10
                if roundNumber == 10:
                    await message.channel.send('{} **Error!** This bot is currently limited to doing up to 10 rounds of swiss. If you need this bot to do more, please contact @vmnunes on discord or smogon.'.format(f'{message.author.mention}'))
                else:
                    if roundNumber == 0: 
                        #if it is the first round, generate a randomized list
                        random.shuffle(playerList) # shuffles the list
                        for count in range(int((len(playerList))/2)):
                            emptyCell = first_empty_cell(dataSpreadsheet,1,1) # get first empty row in match history
                            if count == 0: # if it's the first pairing, get index 0 and 1 on player list
                                player1 = playerList[0][0]
                                player1uid = playerList[0][4]
                                player2 = playerList[1][0]
                                player2uid = playerList[1][4]
                                player1losses = playerList[0][5]
                                player2losses = playerList[1][5]
                            else: # if it's not the first pairing, use the count of pairings generated to get the index numbers of players in the list
                                player1 = playerList[(count*2)][0]
                                player1uid = playerList[(count*2)][4]
                                player2 = playerList[(count*2)+1][0]
                                player2uid = playerList[(count*2)+1][4]
                                player1losses = playerList[(count*2)][5]
                                player2losses = playerList[(count*2)+1][5]
                            create_matchup(player1,player1uid,player2,player2uid,emptyCell,count,updatedRoundNumber,updateRequests,dataId,matchupId,player1losses,player2losses) # create matchup sheet update request
                    else:
                        # if it's not the first round, generate a list based on standings, excluding repeated matchups and selecting a random opponent if there are two or more valid pairings
                        while len(playerList) > 0:
                            emptyCell = first_empty_cell(dataSpreadsheet,1,1) # get first empty row in match history
                            player2bye = False

                            #get player 1
                            player1 = playerList[0][0]
                            # player1wins = playerList[0][2] # not used anymore
                            player1uid = playerList[0][4]
                            player1losses = playerList[0][5]

                            # check if a bye was picked up as player 1
                            if str(playerList[0][0]).startswith('Bye') and len(playerList[0][0]) <= 5:
                                player1isBye = True
                            else:
                                player1isBye = False

                            # generate list of previous matchups
                            previouslyPlayed = []
                            if roundNumber == 1:
                                if 'formattedValue' in dataSpreadsheet['sheets'][0]['data'][0]['rowData'][int(player1uid)]['values'][9].keys(): # check to see if value exists
                                    tempUid = dataSpreadsheet['sheets'][0]['data'][0]['rowData'][int(player1uid)]['values'][9]['formattedValue']
                                    previouslyPlayed.append(tempUid)
                            else:
                                for i in range(0,(roundNumber)):
                                    if 'formattedValue' in dataSpreadsheet['sheets'][0]['data'][0]['rowData'][int(player1uid)]['values'][(i+9)].keys(): # check to see if value exists
                                        tempUid = dataSpreadsheet['sheets'][0]['data'][0]['rowData'][int(player1uid)]['values'][(i+9)]['formattedValue']
                                        previouslyPlayed.append(tempUid)
                            del playerList[0] # remove player 1 from the player list

                            # generate list of valid matchups for this round
                            validMatchups = []
                            for i in range(len(playerList)):
                                # get the W/Res we're trying to match player 1 with
                                if i == 0:
                                    for z in range(len(playerList)):
                                        if playerList[z][4] not in previouslyPlayed:
                                            targetWins = playerList[z][2]
                                            targetRes = playerList[z][3]
                                            # prevent bye from matching up with bye
                                            if player1isBye:
                                                if not (str(playerList[z][0]).startswith('Bye') and len(playerList[z][0]) <= 5):
                                                    validMatchups.append(playerList[z])
                                                    break
                                            else:
                                                validMatchups.append(playerList[z])
                                                break
                                else:
                                    # check if other players have the same W/Res scores
                                    if playerList[i][2] == targetWins and playerList[i][3] == targetRes:
                                        if playerList[i][4] not in previouslyPlayed:
                                            # prevent bye from matching up with bye
                                            if player1isBye:
                                                if not (str(playerList[z][0]).startswith('Bye') and len(playerList[z][0]) <= 5):
                                                    validMatchups.append(playerList[i])
                                            else:
                                                validMatchups.append(playerList[i])
                                    else:
                                        break

                            # get player 2        
                            if len(validMatchups) == 0:
                                # if this is not a round with an odd number of players, output an error if a valid matchup is not found, else generate a bye
                                if not oddRound:
                                    await message.channel.send('{}**Warning!** Could not find a valid matchup for player {}! Are you running too many rounds of swiss for your player pool size? (If you think this is an error, please contact @vmnunes on discord or smogon)'.format(f'{message.author.mention}',str(player1)))
                                else:
                                    player2 = 'BYE'
                                    player2uid = '-'
                                    player2losses = '0'
                                    # player2wins = '0' # no longer used
                                    player2bye = True
                            else:
                                # pick a random player from the list of valid matchups to be player 2
                                if player2bye == False:
                                    randomPick = random.randint(0,(len(validMatchups)-1))
                                    player2 = validMatchups[randomPick][0]
                                    player2uid = validMatchups[randomPick][4]
                                    # player2wins = validMatchups[randomPick][2] #not used anymore
                                    player2losses = validMatchups[randomPick][5]
                                    player2index = 0
                                    for i in range(len(playerList)):
                                        if playerList[i][4] == player2uid:
                                            player2index = i
                                            break
                                    del playerList[player2index]
                            
                            #invert player 1 and player 2 if player 1 is bye
                            if player1isBye:
                                player1temp = player1
                                player1uidTemp = player1uid
                                player1lossesTemp = player1losses
                                player1 = player2
                                player1uid = player2uid
                                player1losses = player2losses
                                player2 = player1temp
                                player2uid = player1uidTemp
                                player2losses = player1lossesTemp
                            # if not int(player1losses) >= lossesCutoff and not int(player2losses) >= lossesCutoff and not int(player1wins) >= 8 and not int(player2wins) >=8: #old version of the check
                            create_matchup(player1,player1uid,player2,player2uid,emptyCell,count,updatedRoundNumber,updateRequests,dataId,matchupId,player1losses,player2losses)
                            count += 1

                    
                    # create body of sheet update request
                    roundUpdate = {
                        "requests": updateRequests 
                    }

                    # send the batch update request to the doc  
                    spreadsheet_service.spreadsheets().batchUpdate(spreadsheetId=message_args[0], body=roundUpdate).execute()


client.run(config['token'])