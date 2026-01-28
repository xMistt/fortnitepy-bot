"""
“Commons Clause” License Condition v1.0
Copyright Oli 2019-2023

The Software is provided to you by the Licensor under the
License, as defined below, subject to the following condition.

Without limiting other conditions in the License, the grant
of rights under the License will not include, and the License
does not grant to you, the right to Sell the Software.

For purposes of the foregoing, “Sell” means practicing any or
all of the rights granted to you under the License to provide
to third parties, for a fee or other consideration (including
without limitation fees for hosting or consulting/ support
services related to the Software), a product or service whose
value derives, entirely or substantially, from the functionality
of the Software. Any license notice or attribution required by
the License must also include this Commons Clause License
Condition notice.

Software: PartyBot (fortnitepy-bot)

License: Apache 2.0
"""

# System imports.
import asyncio
import functools

from typing import Optional, Union, Tuple

# Third party imports.
import rebootpy
import aiohttp
import FortniteAPIAsync
import random as py_random

from rebootpy.ext import commands


class CosmeticCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.name = 'Cosmetic'

    # async def set_vtid(self, variant_token: str) -> Tuple[str, str, int]:
    #     async with aiohttp.ClientSession() as session:
    #         request = await session.request(
    #             method='GET',
    #             url='https://benbot.app/api/v1/assetProperties',
    #             params={
    #                 'path': 'FortniteGame/Content/Athena/'
    #                         f'Items/CosmeticVariantTokens/{variant_token}.uasset'
    #             })
    #
    #         response = await request.json()
    #
    #     file_location = response['export_properties'][0]
    #
    #     skin_cid = file_location['cosmetic_item']
    #     variant_channel_tag = file_location['VariantChanelTag']['TagName']
    #     variant_name_tag = file_location['VariantNameTag']['TagName']
    #
    #     variant_type = variant_channel_tag.split(
    #         'Cosmetics.Variant.Channel.'
    #     )[1].split('.')[0]
    #
    #     variant_int = int("".join(filter(
    #         lambda x: x.isnumeric(), variant_name_tag
    #     )))
    #
    #     return skin_cid, variant_type if variant_type != 'ClothingColor' else 'clothing_color', variant_int

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client using the outfits name.",
        help="Sets the outfit of the client using the outfits name.\n"
             "Example: !skin Nog Ops",
        usage="!skin <content>"
    )
    async def skin(self, ctx: rebootpy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.bot.fortnite_api.cosmetics.get_cosmetic(
                matchMethod="contains",
                name=content,
                backendType="AthenaCharacter"
            )
        except FortniteAPIAsync.exceptions.NotFound:
            print(self.bot.message % f"Failed to find a skin with the name: {content}.")
            return await ctx.send(f"Failed to find a skin with the name: {content}.")

        await self.bot.party.me.set_outfit(asset=cosmetic.id)

        await ctx.send(f'Skin set to {cosmetic.id}.')
        print(self.bot.message % f"Set skin to: {cosmetic.id}.")


    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the backpack of the client using the backpacks name.",
        help="Sets the backpack of the client using the backpacks name.\n"
             "Example: !backpack Black Shield",
        usage="!backpack <content>"
    )
    async def backpack(self, ctx: rebootpy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.bot.fortnite_api.cosmetics.get_cosmetic(
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
        except FortniteAPIAsync.exceptions.NotFound:
            print(self.bot.message % f"Failed to find a backpack with the name: {content}.")
            return await ctx.send(f"Failed to find a backpack with the name: {content}.")

        await self.bot.party.me.set_backpack(asset=cosmetic.id)

        await ctx.send(f'Backpack set to {cosmetic.id}.')
        print(self.bot.message % f"Set backpack to: {cosmetic.id}.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the emote of the client using the emotes name.",
        help="Sets the emote of the client using the emotes name.\n"
             "Example: !emote Windmill Floss",
        usage="!emote <content>"
    )
    async def emote(self, ctx: rebootpy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.bot.fortnite_api.cosmetics.get_cosmetic(
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
        except FortniteAPIAsync.exceptions.NotFound:
            print(self.bot.message % f"Failed to find an emote with the name: {content}.")
            return await ctx.send(f"Failed to find an emote with the name: {content}.")

        await self.bot.party.me.clear_emote()
        await self.bot.party.me.set_emote(asset=cosmetic.id)

        await ctx.send(f'Emote set to {cosmetic.id}.')
        print(self.bot.message % f"Set emote to: {cosmetic.id}.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the pickaxe of the client using the pickaxe name.",
        help="Sets the pickaxe of the client using the pickaxe name.\n"
             "Example: !pickaxe Raider's Revenge",
        usage="!pickaxe <content>"
    )
    async def pickaxe(self, ctx: rebootpy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.bot.fortnite_api.cosmetics.get_cosmetic(
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
        except FortniteAPIAsync.exceptions.NotFound:
            print(self.bot.message % f"Failed to find a pickaxe with the name: {content}.")
            return await ctx.send(f"Failed to find a pickaxe with the name: {content}.")

        await self.bot.party.me.set_pickaxe(asset=cosmetic.id)

        await ctx.send(f'Pickaxe set to {cosmetic.id}.')
        print(self.bot.message % f"Set pickaxe to: {cosmetic.id}.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the pet (backpack) of the client using the pets name.",
        help="Sets the pet (backpack) of the client using the pets name.\n"
             "Example: !pet Bonesy",
        usage="!pet <content>"
    )
    async def pet(self, ctx: rebootpy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.bot.fortnite_api.cosmetics.get_cosmetic(
                matchMethod="contains",
                name=content,
                backendType="AthenaPetCarrier"
            )
        except FortniteAPIAsync.exceptions.NotFound:
            print(self.bot.message % f"Failed to find a pet with the name: {content}.")
            return await ctx.send(f"Failed to find a pet with the name: {content}.")

        await self.bot.party.me.set_pet(asset=cosmetic.id)

        await ctx.send(f'Pet set to {cosmetic.id}.')
        print(self.bot.message % f"Set pet to: {cosmetic.id}.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the emoji of the client using the emojis name.",
        help="Sets the emoji of the client using the emojis name.\n"
             "Example: !emoji On Fire",
        usage="!emoji <content>"
    )
    async def emoji(self, ctx: rebootpy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.bot.fortnite_api.cosmetics.get_cosmetic(
                matchMethod="contains",
                name=content,
                backendType="AthenaEmoji"
            )
        except FortniteAPIAsync.exceptions.NotFound:
            print(self.bot.message % f"Failed to find an emoji with the name: {content}.")
            return await ctx.send(f"Failed to find an emoji with the name: {content}.")

        await self.bot.party.me.clear_emote()
        await self.bot.party.me.set_emoji(asset=cosmetic.id)

        await ctx.send(f'Emoji set to {cosmetic.id}.')
        print(self.bot.message % f"Set emoji to: {cosmetic.id}.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the contrail of the client using the contrail name.",
        help="Sets the contrail of the client using the contrail name.\n"
             "Example: !contrail Holly And Divey",
        usage="!contrail <content>"
    )
    async def contrail(self, ctx: rebootpy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.bot.fortnite_api.cosmetics.get_cosmetic(
                matchMethod="contains",
                name=content,
                backendType="AthenaSkyDiveContrail"
            )
        except FortniteAPIAsync.exceptions.NotFound:
            print(self.bot.message % f"Failed to find an contrail with the name: {content}.")
            return await ctx.send(f"Failed to find a contrail with the name: {content}.")

        await self.bot.party.me.set_contrail(asset=cosmetic.id)

        await ctx.send(f'Contrail set to {cosmetic.id}.')
        print(self.bot.message % f"Set contrail to: {cosmetic.id}.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to Purple Skull Trooper.",
        help="Sets the outfit of the client to Purple Skull Trooper.\n"
             "Example: !purpleskull",
        usage="!purpleskull"
    )
    async def purpleskull(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=['0|1', '1|1']
        )

        await ctx.send('Skin set to Purple Skull Trooper!')
        print(self.bot.message % f"Skin set to Purple Skull Trooper.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to Pink Ghoul Trooper.",
        help="Sets the outfit of the client to Pink Ghoul Trooper.\n"
             "Example: !pinkghoul",
        usage="!pinkghoul"
    )
    async def pinkghoul(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=["0|2"]
        )

        await ctx.send('Skin set to Pink Ghoul Trooper!')
        print(self.bot.message % f"Skin set to Pink Ghoul Trooper.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the backpack of the client to Purple Ghost Portal.",
        help="Sets the backpack of the client to Purple Ghost Portal.\n"
             "Example: !purpleportal",
        usage="!purpleportal"
    )
    async def purpleportal(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_backpack(
            asset='BID_105_GhostPortal',
            variants=['0|1']
        )

        await ctx.send('Backpack set to Purple Ghost Portal!')
        print(self.bot.message % f"Backpack set to Purple Ghost Portal.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client using CID.",
        help="Sets the outfit of the client using CID.\n"
             "Example: !cid CID_047_Athena_Commando_F_HolidayReindeer",
        usage="!cid <character_id>"
    )
    async def cid(self, ctx: rebootpy.ext.commands.Context, character_id: str) -> None:
        await self.bot.party.me.set_outfit(
            asset=character_id,
            variants=self.bot.party.me.create_variants(profile_banner='ProfileBanner')
        )

        await ctx.send(f'Skin set to {character_id}.')
        print(self.bot.message % f'Skin set to {character_id}.')

    # NOTE: Command is currently not possible due to no APIs allowing you to browse the files, hope to fix eventually.
    # @commands.dm_only()
    # @commands.command(
    #     description="[Cosmetic] Creates the variants list by the variants you set using VTID.",
    #     help="Creates the variants list by the variants you set using VTID.\n"
    #          "Example: !vtid VTID_052_Skull_Trooper_RedFlames"
    # )
    # async def vtid(self, ctx: rebootpy.ext.commands.Context, variant_token: str) -> None:
    #     variant_id = await self.set_vtid(variant_token)
    #
    #     if variant_id[1].lower() == 'particle':
    #         skin_variants = self.bot.party.me.create_variants(config_overrides={'particle': 'Particle{}'}, particle=1)
    #     else:
    #         skin_variants = self.bot.party.me.create_variants(**{variant_id[1].lower(): int(variant_id[2])})
    #
    #     await self.bot.party.me.set_outfit(asset=variant_id[0], variants=skin_variants)
    #     print(self.bot.message % f'Set variants of {variant_id[0]} to {variant_id[1]} {variant_id[2]}.')
    #     await ctx.send(f'Variants set to {variant_token}.\n'
    #                    '(Warning: This feature is not supported, please use !variants)')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Creates the variants list by the variants you set.",
        help="Creates the variants list by the variants you set.\n"
             "Example: !variants CID_030_Athena_Commando_M_Halloween 1 1",
        usage="!variants <cosmetic_id> <variant_choice1> <variant_choice2>..."
    )
    async def variants(self,
                       ctx: rebootpy.ext.commands.Context,
                       cosmetic_id: str,
                       *variant_choices: int
                       ) -> None:
        if cosmetic_id.lower().startswith('cid_'):
            cosmetic_variants = [
                f"0|{variant_choice}" for variant_choice in variant_choices
            ]

            await self.bot.party.me.set_outfit(
                asset=cosmetic_id,
                variants=cosmetic_variants
            )
        elif cosmetic_id.lower().startswith('bid_'):
            cosmetic_variants = [
                f"0|{variant_choice}" for variant_choice in variant_choices
            ]

            await self.bot.party.me.set_backpack(
                asset=cosmetic_id,
                variants=cosmetic_variants
            )
        elif cosmetic_id.lower().startswith('pickaxe_id_'):
            cosmetic_variants = [
                f"0|{variant_choice}" for variant_choice in variant_choices
            ]

            await self.bot.party.me.set_pickaxe(
                asset=cosmetic_id,
                variants=cosmetic_variants
            )

        await ctx.send(f'Set variants of {cosmetic_id} to {variant_choices}.')
        print(self.bot.message % f'Set variants of {cosmetic_id} to {variant_choices}.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to OG Renegade Raider.",
        help="Sets the outfit of the client to OG Renegade Raider.\n"
             "Example: !ogrene",
        usage="!ogrene"
    )
    async def ogrene(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
            variants=['0|2']
        )

        await ctx.send('Skin set to OG Renegade Raider!')
        print(self.bot.message % f'Skin set to OG Renegade Raider.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to OG Aerial Assault Trooper.",
        help="Sets the outfit of the client to OG Aerial Assault Trooper.\n"
             "Example: !ogaerial",
        usage="!ogaerial"
    )
    async def ogaerial(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_017_Athena_Commando_M',
            variants=['0|1']
        )

        await ctx.send('Skin set to OG Aerial Assault Trooper!')
        print(self.bot.message % f'Skin set to OG Aerial Assault Trooper.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to Minty Elf.",
        help="Sets the outfit of the client to Minty Elf.\n"
             "Example: !mintyelf",
        usage="!mintyelf"
    )
    async def mintyelf(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_051_Athena_Commando_M_HolidayElf',
            variants=['0|1']
        )

        await ctx.send('Skin set to Minty Elf!')
        print(self.bot.message % f'Skin set to Minty Elf.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the emote of the client using EID.",
        help="Sets the emote of the client using EID.\n"
             "Example: !eid EID_Floss",
        usage="!eid <emote_id>"
    )
    async def eid(self, ctx: rebootpy.ext.commands.Context, emote_id: str) -> None:
        await self.bot.party.me.clear_emote()
        await self.bot.party.me.set_emote(
            asset=emote_id
        )

        await ctx.send(f'Emote set to {emote_id}!')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Clears/stops the emote currently playing.",
        help="Clears/stops the emote currently playing.\n"
             "Example: !stop",
        usage="!stop"
    )
    async def stop(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.clear_emote()
        await ctx.send('Stopped emoting.')
        print(self.bot.message % f'Stopped emoting.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the backpack of the client using BID.",
        help="Sets the backpack of the client using BID.\n"
             "Example: !bid BID_023_Pinkbear",
        usage="!bid <backpack_id>"
    )
    async def bid(self, ctx: rebootpy.ext.commands.Context, backpack_id: str) -> None:
        await self.bot.party.me.set_backpack(
            asset=backpack_id
        )

        await ctx.send(f'Backbling set to {backpack_id}!')
        print(self.bot.message % f'Backbling set to {backpack_id}!')

    @commands.dm_only()
    @commands.command(
        aliases=['legacypickaxe'],
        description="[Cosmetic] Sets the pickaxe of the client using PICKAXE_ID",
        help="Sets the pickaxe of the client using PICKAXE_ID\n"
             "Example: !pickaxe_id Pickaxe_ID_073_Balloon",
        usage="!pickaxe_id <pickaxe_id_>"
    )
    async def pickaxe_id(self, ctx: rebootpy.ext.commands.Context, pickaxe_id_: str) -> None:
        await self.bot.party.me.set_pickaxe(
            asset=pickaxe_id_
        )

        await ctx.send(f'Pickaxe set to {pickaxe_id_}')
        print(self.bot.message % f'Pickaxe set to {pickaxe_id_}')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the pet of the client using PetCarrier_.",
        help="Sets the pet of the client using PetCarrier_.\n"
             "Example: !pet_carrier PetCarrier_002_Chameleon",
        usage="!pet_carrier <pet_carrier_id>"
    )
    async def pet_carrier(self, ctx: rebootpy.ext.commands.Context, pet_carrier_id: str) -> None:
        await self.bot.party.me.set_pet(
            asset=pet_carrier_id
        )

        await ctx.send(f'Pet set to {pet_carrier_id}!')
        print(self.bot.message % f'Pet set to {pet_carrier_id}!')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the emoji of the client using Emoji_.",
        help="Sets the emoji of the client using Emoji_.\n"
             "Example: !emoji_id Emoji_PeaceSign",
        usage="!emoji_id <emoji_>"
    )
    async def emoji_id(self, ctx: rebootpy.ext.commands.Context, emoji_: str) -> None:
        await self.bot.party.me.clear_emote()
        await self.bot.party.me.set_emoji(
            asset=emoji_
        )

        await ctx.send(f'Emoji set to {emoji_}!')
        print(self.bot.message % f'Emoji set to {emoji_}!')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the contrail of the client using Trails_.",
        help="Sets the contrail of the client using Trails_.\n"
             "Example: !trails Trails_ID_075_Celestial",
        usage="!trails <trails_>"
    )
    async def trails(self, ctx: rebootpy.ext.commands.Context, trails_: str) -> None:
        await self.bot.party.me.set_contrail(
            asset=trails_
        )

        await ctx.send(f'Contrail set to {trails_}!')
        print(self.bot.message % f'Contrail set to {trails_}!')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets pickaxe using PICKAXE_ID or display name & does 'Point it Out'. If no pickaxe is "
                    "specified, only the emote will be played.",
        help="Sets pickaxe using PICKAXE_ID or display name & does 'Point it Out'. If no pickaxe is "
             "specified, only the emote will be played.\n"
             "Example: !point Pickaxe_ID_029_Assassin",
        usage="!point <content>"
    )
    async def point(self, ctx: rebootpy.ext.commands.Context, *, content: Optional[str] = None) -> None:
        if content is None:
            await self.bot.party.me.set_emote(asset='EID_None')
            await self.bot.party.me.set_emote(asset='EID_IceKing')
            await ctx.send(f'Point it Out played.')
        elif 'pickaxe_id' in content.lower():
            await self.bot.party.me.set_pickaxe(asset=content)
            await self.bot.party.me.set_emote(asset='EID_None')
            await self.bot.party.me.set_emote(asset='EID_IceKing')
            await ctx.send(f'Pickaxe set to {content} & Point it Out played.')
        else:
            try:
                cosmetic = await self.bot.fortnite_api.cosmetics.get_cosmetic(
                    matchMethod="contains",
                    name=content,
                    backendType="AthenaPickaxe"
                )
            except FortniteAPIAsync.exceptions.NotFound:
                print(self.bot.message % f"Failed to find a pickaxe with the name: {content}.")
                return await ctx.send(f"Failed to find a pickaxe with the name: {content}.")

            await self.bot.party.me.set_pickaxe(asset=cosmetic.id)

            await self.bot.party.me.set_emote(asset='EID_None')
            await self.bot.party.me.set_emote(asset='EID_IceKing')

            await ctx.send(f'Pickaxe set to {content} & Point it Out played.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Copies the cosmetic loadout of the defined user. If user is left blank, "
                    "the message author will be used.",
        help="Copies the cosmetic loadout of the defined user. If user is left blank, "
             "the message author will be used.\n"
             "Example: !copy Terbau",
        usage="!copy <epic_username>"
    )
    async def copy(self, ctx: rebootpy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        if epic_username is None:
            member = [m for m in self.bot.party.members if m.id == ctx.author.id][0]
        else:
            member = [m for m in self.bot.party.members if m.display_name == epic_username][0]

        await self.bot.party.me.edit(
            functools.partial(
                rebootpy.ClientPartyMember.set_outfit,
                asset=member.outfit,
                variants=member.outfit_variants
            ),
            functools.partial(
                rebootpy.ClientPartyMember.set_backpack,
                asset=member.backpack,
                variants=member.backpack_variants
            ),
            functools.partial(
                rebootpy.ClientPartyMember.set_pickaxe,
                asset=member.pickaxe,
                variants=member.pickaxe_variants
            ),
            functools.partial(
                rebootpy.ClientPartyMember.set_banner,
                icon=member.banner[0],
                color=member.banner[1],
                season_level=member.banner[2]
            ),
            functools.partial(
                rebootpy.ClientPartyMember.set_battlepass_info,
                has_purchased=True,
                level=member.battlepass_info[1]
            )
        )

        if member.emote is not None:
            await self.bot.party.me.set_emote(asset=member.emote)

        await ctx.send(f'Copied the loadout of {member.display_name}.')
        print(self.bot.message % f'Copied the loadout of {member.display_name}.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Shortcut for equipping the skin CID_VIP_Athena_Commando_M_GalileoGondola_SG.",
        help="Shortcut for equipping the skin CID_VIP_Athena_Commando_M_GalileoGondola_SG.\n"
             "Example: !hologram",
        usage="!hologram"
    )
    async def hologram(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
        )

        await ctx.send('Skin set to Star Wars Hologram!')
        print(self.bot.message % f'Skin set to Star Wars Hologram.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Shortcut for equipping the skin CID_VIP_Athena_Commando_M_GalileoGondola_SG.",
        help="Shortcut for equipping the skin CID_VIP_Athena_Commando_M_GalileoGondola_SG.\n"
             "Example: !gift is a joke command.",
        usage="!gift"
    )
    async def gift(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.clear_emote()

        await self.bot.party.me.set_emote(
            asset='EID_NeverGonna'
        )

        await ctx.send('What did you think would happen?')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Shortcut for equipping the emote EID_TourBus.",
        help="Shortcut for equipping the emote EID_TourBus.\n"
             "Example: !ponpon",
        usage="!ponpon"
    )
    async def ponpon(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_emote(
            asset='EID_TourBus'
        )

        await ctx.send('Emote set to Ninja Style!')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the enlightened value of a skin "
                    "(used for skins such as glitched Scratch or Golden Peely).",
        help="Sets the enlightened value of a skin.\n"
             "Example: !enlightened CID_701_Athena_Commando_M_BananaAgent 2 350",
        usage="!enlightened <cosmetic_id> <br_season> <skin_level>"
    )
    async def enlightened(self,
                          ctx: rebootpy.ext.commands.Context,
                          cosmetic_id: str,
                          br_season: int,
                          skin_level: int
                          ) -> None:
        variant_types = {
            1: ['0|3'],
            2: ['0|3'],
            3: ['0|0', '1|1', '2|0']
        }

        if 'cid' in cosmetic_id.lower():
            await self.bot.party.me.set_outfit(
                asset=cosmetic_id,
                variants=variant_types[br_season] if br_season in variant_types else variant_types[2],
                enlightenment=(br_season, skin_level)
            )

            await ctx.send(f'Skin set to {cosmetic_id} at level {skin_level} (for Season 1{br_season}).')
        elif 'bid' in cosmetic_id.lower():
            await self.bot.party.me.set_backpack(
                asset=cosmetic_id,
                variants=self.bot.party.me.create_variants(progressive=2),
                enlightenment=(br_season, skin_level)
            )
            await ctx.send(f'Backpack set to {cosmetic_id} at level {skin_level} (for Season 1{br_season}).')

        print(
            self.bot.message % f'Enlightenment for {cosmetic_id} set to level {skin_level} '
            f'(for Season 1{br_season}).'
        )

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Shortcut for equipping the skin CID_605_Athena_Commando_M_TourBus.",
        help="Shortcut for equipping the skin CID_605_Athena_Commando_M_TourBus.\n"
             "Example: !ninja",
        usage="!ninja"
    )
    async def ninja(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_605_Athena_Commando_M_TourBus'
        )

        await ctx.send('Skin set to Ninja!')
        print(self.bot.message % f'Skin set to Ninja.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Equips all very rare skins.",
        help="Equips all very rare skins.\n"
             "Example: !rareskins",
        usage="!rareskins"
    )
    async def rareskins(self, ctx: rebootpy.ext.commands.Context) -> None:
        await ctx.send('Showing all rare skins now.')

        await self.bot.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=['0|1', '1|1']
        )

        await ctx.send('Skin set to Purple Skull Trooper!')
        print(self.bot.message % f"Skin set to Purple Skull Trooper.")
        await asyncio.sleep(2)

        await self.bot.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=["0|2"]
        )

        await ctx.send('Skin set to Pink Ghoul Trooper!')
        print(self.bot.message % f"Skin set to Pink Ghoul Trooper.")
        await asyncio.sleep(2)

        await self.bot.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
            variants=['0|2']
        )

        await ctx.send('Skin set to OG Renegade Raider!')
        print(self.bot.message % f"Skin set to OG Renegade Raider.")
        await asyncio.sleep(2)

        await self.bot.party.me.set_outfit(
            asset='CID_017_Athena_Commando_M',
            variants=['0|1']
        )

        await ctx.send('Skin set to OG Aerial Assault Trooper!')
        print(self.bot.message % f"Skin set to OG Aerial Assault Trooper.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to Golden Peely "
                    "(shortcut for !enlightened CID_701_Athena_Commando_M_BananaAgent 2 350).",
        help="Sets the outfit of the client to Golden Peely.\n"
             "Example: !goldenpeely",
        usage="!goldenpeely"
    )
    async def goldenpeely(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_701_Athena_Commando_M_BananaAgent',
            variants=['0|3'],
            enlightenment=(2, 350)
        )

        await ctx.send(f'Skin set to Golden Peely.')

    # to fix
    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Randomly finds & equips a skin. Types currently include skin, backpack, emote & all. "
                    "If type is left blank, a random skin will be equipped.",
        help="Randomly finds & equips a skin.\n"
             "Example: !random skin",
        usage="!random <cosmetic_type>"
    )
    async def random(self, ctx: rebootpy.ext.commands.Context, cosmetic_type: str = 'skin') -> None:
        if cosmetic_type == 'skin':
            all_outfits = await self.bot.fortnite_api.cosmetics.get_cosmetics(
                lang="en",
                searchLang="en",
                backendType="AthenaCharacter"
            )

            random_skin = py_random.choice(all_outfits).id

            await self.bot.party.me.set_outfit(
                asset=random_skin,
                variants=self.bot.party.me.create_variants(profile_banner='ProfileBanner')
            )

            await ctx.send(f'Skin randomly set to {random_skin}.')
            print(self.bot.message % f"Set skin randomly to: {random_skin}.")

        elif cosmetic_type == 'backpack':
            all_backpacks = await self.bot.fortnite_api.cosmetics.get_cosmetics(
                lang="en",
                searchLang="en",
                backendType="AthenaBackpack"
            )

            random_backpack = py_random.choice(all_backpacks).id

            await self.bot.party.me.set_backpack(
                asset=random_backpack,
                variants=self.bot.party.me.create_variants(profile_banner='ProfileBanner')
            )

            await ctx.send(f'Backpack randomly set to {random_backpack}.')
            print(self.bot.message % f"Set backpack randomly to: {random_backpack}.")

        elif cosmetic_type == 'emote':
            all_emotes = await self.bot.fortnite_api.cosmetics.get_cosmetics(
                lang="en",
                searchLang="en",
                backendType="AthenaDance"
            )

            random_emote = py_random.choice(all_emotes).id

            await self.bot.party.me.set_emote(
                asset=random_emote
            )

            await ctx.send(f'Emote randomly set to {random_emote}.')
            print(self.bot.message % f"Set emote randomly to: {random_emote}.")

        elif cosmetic_type == 'all':
            all_outfits = await self.bot.fortnite_api.cosmetics.get_cosmetics(
                lang="en",
                searchLang="en",
                backendType="AthenaCharacter"
            )

            all_backpacks = await self.bot.fortnite_api.cosmetics.get_cosmetics(
                lang="en",
                searchLang="en",
                backendType="AthenaBackpack"
            )

            all_emotes = await self.bot.fortnite_api.cosmetics.get_cosmetics(
                lang="en",
                searchLang="en",
                backendType="AthenaDance"
            )

            random_outfit = py_random.choice(all_outfits).id
            random_backpack = py_random.choice(all_backpacks).id
            random_emote = py_random.choice(all_emotes).id

            await self.bot.party.me.set_outfit(
                asset=random_outfit
            )

            await ctx.send(f'Skin randomly set to {random_outfit}.')
            print(self.bot.message % f"Set skin randomly to: {random_outfit}.")

            await self.bot.party.me.set_backpack(
                asset=random_backpack
            )

            await ctx.send(f'Backpack randomly set to {random_backpack}.')
            print(self.bot.message % f"Set backpack randomly to: {random_backpack}.")

            await self.bot.party.me.set_emote(
                asset=random_emote
            )

            await ctx.send(f'Emote randomly set to {random_emote}.')
            print(self.bot.message % f"Set emote randomly to: {random_emote}.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Clears the currently set backpack.",
        help="Clears the currently set backpack.\n"
             "Example: !nobackpack",
        usage="!nobackpack"
    )
    async def nobackpack(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.clear_backpack()
        await ctx.send('Removed backpack.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Clears the currently set pet.",
        help="Clears the currently set pet.\n"
             "Example: !nopet",
        usage="!nopet"
    )
    async def nopet(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.clear_pet()
        await ctx.send('Removed pet.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Clears the currently set contrail.",
        help="Clears the currently set contrail.\n"
             "Example: !nocontrail",
        usage="!nocontrail"
    )
    async def nocontrail(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.clear_contrail()
        await ctx.send('Removed contrail.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client using the outfits name with the ghost variant.",
        help="Sets the outfit of the client using the outfits name with the ghost variant.\n"
             "Example: !ghost Meowscles",
        usage="!ghost <content>"
    )
    async def ghost(self, ctx: rebootpy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.bot.fortnite_api.cosmetics.get_cosmetic(
                matchMethod="contains",
                name=content,
                backendType="AthenaCharacter"
            )

            await self.bot.party.me.set_outfit(
                asset=cosmetic.id,
                variants=['0|1']
            )

            await ctx.send(f'Skin set to Ghost {cosmetic.name}!')
            print(self.bot.message % f'Skin set to Ghost {cosmetic.name}.')
        except FortniteAPIAsync.exceptions.NotFound:
            print(self.bot.message % f"Failed to find a skin with the name: {content}.")
            return await ctx.send(f"Failed to find a skin with the name: {content}.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client using the outfits name with the shadow variant.",
        help="Sets the outfit of the client using the outfits name with the shadow variant.\n"
             "Example: !shadow Midas",
        usage="!shadow <content>"
    )
    async def shadow(self, ctx: rebootpy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.bot.fortnite_api.cosmetics.get_cosmetic(
                matchMethod="contains",
                name=content,
                backendType="AthenaCharacter"
            )

            await self.bot.party.me.set_outfit(
                asset=cosmetic.id,
                variants=['0|2']
            )

            await ctx.send(f'Skin set to Shadow {cosmetic.name}!')
            print(self.bot.message % f'Skin set to Ghost {cosmetic.name}.')
        except FortniteAPIAsync.exceptions.NotFound:
            print(self.bot.message % f"Failed to find a skin with the name: {content}.")
            return await ctx.send(f"Failed to find a skin with the name: {content}.")

    # to fix
    @commands.dm_only()
    @commands.command(
        name="set",
        description="[Cosmetic] Equips all cosmetics from a set.",
        help="Equips all cosmetics from a set.\n"
             "Example: !set Fort Knights"
    )
    async def _set(self, ctx: rebootpy.ext.commands.Context, *, content: str) -> None:
        cosmetic_types = {
            "AthenaBackpack": self.bot.party.me.set_backpack,
            "AthenaCharacter": self.bot.party.me.set_outfit,
            "AthenaEmoji": self.bot.party.me.set_emoji,
            "AthenaDance": self.bot.party.me.set_emote
        }

        set_items = await self.bot.fortnite_api.cosmetics.get_cosmetics(
            matchMethod="contains",
            set=content
        )

        await ctx.send(f'Equipping all cosmetics from the {set_items[0].set["value"]} set.')
        print(self.bot.message % f'Equipping all cosmetics from the {set_items[0].set["value"]} set.')

        for cosmetic in set_items:
            if cosmetic.type['backendValue'] in cosmetic_types:
                await cosmetic_types[cosmetic.type['backendValue']](asset=cosmetic.id)

                await ctx.send(f'{cosmetic.type["value"].capitalize()} set to {cosmetic.name}!')
                print(self.bot.message % f'{cosmetic.type["value"].capitalize()} set to {cosmetic.name}.')

                await asyncio.sleep(3)

        await ctx.send(f'Finished equipping all cosmetics from the {set_items[0].set["value"]} set.')
        print(self.bot.message % f'Fishing equipping  all cosmetics from the {set_items[0].set["value"]} set.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Creates the variants list by the variants you set from skin name. "
                    "If you want to include spaces in the skin name, you need to enclose it in \"'s.",
        help="Creates the variants list by the variants you set from skin name.\n"
             "Example: !style \"Skull Trooper\" 1 1",
        usage='!style "<cosmetic_name>" <variant_choice1> <variant_choice2>...'
    )
    async def style(self,
                    ctx: rebootpy.ext.commands.Context,
                    cosmetic_name: str,
                    *variant_choices: int) -> None:
        # cosmetic_types = {
        #     "AthenaCharacter": self.bot.party.me.set_outfit,
        #     "AthenaBackpack": self.bot.party.me.set_backpack,
        #     "AthenaPickaxe": self.bot.party.me.set_pickaxe
        # }

        cosmetic = await self.bot.fortnite_api.cosmetics.get_cosmetic(
            matchMethod="contains",
            name=cosmetic_name,
            backendType="AthenaCharacter"
        )

        cosmetic_variants = [
            f"0|{variant_choice}" for variant_choice in variant_choices
        ]

        # await cosmetic_types[cosmetic.backend_type.value](
        await self.bot.party.me.set_outfit(
            asset=cosmetic.id,
            variants=cosmetic_variants
        )

        await ctx.send(f'Set variants of {cosmetic.id} to {cosmetic_variants}.')
        print(self.bot.message % f'Set variants of {cosmetic.id} to {cosmetic_variants}.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Equips all new non encrypted cosmetics.",
        help="Equips all new non encrypted cosmetics.\n"
             "Example: !new",
        usage="!new"
    )
    async def new(self, ctx: rebootpy.ext.commands.Context, cosmetic_type: str = 'skins') -> None:
        cosmetic_types = {
            'skins': {
                'id': 'AthenaCharacter',
                'function': self.bot.party.me.set_outfit
            },
            'backpacks': {
                'id': 'AthenaBackpack',
                'function': self.bot.party.me.set_backpack
            },
            'emotes': {
                'id': 'AthenaDance',
                'function': self.bot.party.me.set_emote
            },
        }

        if cosmetic_type not in cosmetic_types:
            return await ctx.send('Invalid cosmetic type, valid types include: skins, backpacks & emotes.')

        new_cosmetics = await self.bot.fortnite_api.cosmetics.get_new_cosmetics()

        for new_id in new_cosmetics:
            print(new_id.type)

        for new_cosmetic in [
            new_id for new_id in new_cosmetics
            if new_id.type['backendValue'] == cosmetic_types[cosmetic_type]['id']
        ]:
            await cosmetic_types[cosmetic_type]['function'](
                asset=new_cosmetic.id
            )

            await ctx.send(f"{cosmetic_type[:-1].capitalize()} set to {new_cosmetic.id}.")
            print(self.bot.message % f"{cosmetic_type[:-1].capitalize()} set to: {new_cosmetic.id}.")

            await asyncio.sleep(3)

        await ctx.send(f'Finished equipping all new unencrypted {cosmetic_type}.')
        print(self.bot.message % f'Finished equipping all new unencrypted {cosmetic_type}.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Equips all skins currently in the item shop.",
        help="Equips all skins currently in the item shop.\n"
             "Example: !shop",
        usage="!shop"
    )
    async def shop(self, ctx: rebootpy.ext.commands.Context) -> None:
        store = await self.bot.fetch_item_shop()

        await ctx.send(f"Equipping all skins in today's item shop.")
        print(self.bot.message % f"Equipping all skins in today's item shop.")

        assets = list(set([
            grant['asset']
            for item in store.items
            for grant in item.grants
            if grant.get('type') == 'AthenaCharacter'
        ]))

        for asset in assets:
            await self.bot.party.me.set_outfit(asset)
            await ctx.send(f"Skin set to {asset}!")
            print(self.bot.message % f"Skin set to: {asset}!")

            await asyncio.sleep(3)

        await ctx.send(f'Finished equipping all skins in the item shop.')
        print(self.bot.message % f'Finished equipping all skins in the item shop.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Equips a random old default skin.",
        help="Equips a random old default skin.\n"
             "Example: !olddefault",
        usage="!olddefault"
    )
    async def olddefault(self, ctx: rebootpy.ext.commands.Context) -> None:
        random_default = py_random.choice(
            [cid_ for cid_ in dir(rebootpy.DefaultCharactersChapter1) if not cid_.startswith('_')]
        )

        await self.bot.party.me.set_outfit(
            asset=random_default
        )

        await ctx.send(f'Skin set to {random_default}!')
        print(self.bot.message % f"Skin set to {random_default}.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to Hatless Recon Expert.",
        help="Sets the outfit of the client to Hatless Recon Expert.\n"
             "Example: !hatlessrecon",
        usage="!hatlessrecon"
    )
    async def hatlessrecon(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_022_Athena_Commando_F',
            variants=['0|1']
        )

        await ctx.send('Skin set to Hatless Recon Expert!')
        print(self.bot.message % f'Skin set to Hatless Recon Expert.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the to the max tier skin in the defined season.",
        help="Sets the outfit of the to the max tier skin in the defined season.\n"
             "Example: !season 2",
        usage="!season <br_season>"
    )
    async def season(self, ctx: rebootpy.ext.commands.Context, br_season: int) -> None:
        max_tier_skins = {
            1: "CID_028_Athena_Commando_F",
            2: "CID_035_Athena_Commando_M_Medieval",
            3: "CID_084_Athena_Commando_M_Assassin",
            4: "CID_116_Athena_Commando_M_CarbideBlack",
            5: "CID_165_Athena_Commando_M_DarkViking",
            6: "CID_230_Athena_Commando_M_Werewolf",
            7: "CID_288_Athena_Commando_M_IceKing",
            8: "CID_352_Athena_Commando_F_Shiny",
            9: "CID_407_Athena_Commando_M_BattleSuit",
            10: "CID_484_Athena_Commando_M_KnightRemix",
            11: "CID_572_Athena_Commando_M_Viper",
            12: "CID_694_Athena_Commando_M_CatBurglar",
            13: "CID_767_Athena_Commando_F_BlackKnight",
            14: "CID_843_Athena_Commando_M_HightowerTomato_Casual",
            15: "CID_967_Athena_Commando_M_AncientGladiator",
            16: "CID_A_038_Athena_Commando_F_TowerSentinel",
            17: "CID_A_112_Athena_Commando_M_Ruckus",
            18: "CID_A_197_Athena_Commando_M_Clash",
            19: "CID_572_Athena_Commando_M_Viper",
            20: "CID_A_367_Athena_Commando_M_Mystic",
            21: "CID_A_422_Athena_Commando_M_Realm",
            22: "Character_RoseDust",
            23: "Character_Citadel",
            24: "Character_NitroFlow",
            25: "Character_LoudPhoenix",
            26: "Character_LazarusLens",
            27: "Character_HornedJudgment_Midgard",
            28: "Character_ZebraScramble_Bacon",
            29: "Character_DarkStance_Inferno",
            30: "Character_MegaToof_Valve",
            31: "Character_SnapFreeze_Hunt",
            32: "Character_GoldCat_Claw",
            33: "Character_RoseDepth_Seed"
        }

        await self.bot.party.me.set_outfit(asset=max_tier_skins[br_season])

        await ctx.send(f'Skin set to {max_tier_skins[br_season]}!')
        print(self.bot.message % f"Skin set to {max_tier_skins[br_season]}.")

    @commands.dm_only()
    @commands.command(
        aliases=['henchmen'],
        description="[Cosmetic] Sets the outfit of the client to a random Henchman skin.",
        help="Sets the outfit of the client to a random Henchman skin.\n"
             "Example: !henchman",
        usage="!henchman"
    )
    async def henchman(self, ctx: rebootpy.ext.commands.Context) -> None:
        random_henchman = py_random.choice(
            [
                "CID_794_Athena_Commando_M_HenchmanBadShorts_D",
                "CID_NPC_Athena_Commando_F_HenchmanSpyDark",
                "CID_791_Athena_Commando_M_HenchmanGoodShorts_D",
                "CID_780_Athena_Commando_M_HenchmanBadShorts",
                "CID_NPC_Athena_Commando_M_HenchmanGood",
                "CID_692_Athena_Commando_M_HenchmanTough",
                "CID_707_Athena_Commando_M_HenchmanGood",
                "CID_792_Athena_Commando_M_HenchmanBadShorts_B",
                "CID_793_Athena_Commando_M_HenchmanBadShorts_C",
                "CID_NPC_Athena_Commando_M_HenchmanBad",
                "CID_790_Athena_Commando_M_HenchmanGoodShorts_C",
                "CID_779_Athena_Commando_M_HenchmanGoodShorts",
                "CID_NPC_Athena_Commando_F_RebirthDefault_Henchman",
                "CID_NPC_Athena_Commando_F_HenchmanSpyGood",
                "CID_706_Athena_Commando_M_HenchmanBad",
                "CID_789_Athena_Commando_M_HenchmanGoodShorts_B"
            ]
        )

        await self.bot.party.me.set_outfit(
            asset=random_henchman
        )

        await ctx.send(f'Skin set to {random_henchman}!')
        print(self.bot.message % f"Skin set to {random_henchman}.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the emote of the client to Floss.",
        help="Sets the emote of the client to Floss.\n"
             "Example: !floss",
        usage="!floss"
    )
    async def floss(self, ctx: rebootpy.ext.commands.Context) -> None:
        # // You caused this FunGames, you caused this...
        await self.bot.party.me.set_emote(
            asset='EID_Floss'
        )

        await ctx.send('Emote set to Floss!')
        print(self.bot.message % f"Emote set to Floss.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to a random marauder skin.",
        help="Sets the outfit of the client to a random marauder skin.\n"
             "Example: !marauder",
        usage="!marauder"
    )
    async def marauder(self, ctx: rebootpy.ext.commands.Context) -> None:
        random_marauder = py_random.choice(
            [
                "CID_NPC_Athena_Commando_M_MarauderHeavy",
                "CID_NPC_Athena_Commando_M_MarauderElite",
                "CID_NPC_Athena_Commando_M_MarauderGrunt"
            ]
        )

        await self.bot.party.me.set_outfit(
            asset=random_marauder
        )

        await ctx.send(f'Skin set to {random_marauder}!')
        print(self.bot.message % f"Skin set to {random_marauder}.")

    @commands.dm_only()
    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to Golden Brutus "
                    "(shortcut for !enlightened CID_692_Athena_Commando_M_HenchmanTough 2 180).",
        help="Sets the outfit of the client to Golden Brutus.\n"
             "Example: !goldenbrutus",
        usage="!goldenbrutus"
    )
    async def goldenbrutus(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_692_Athena_Commando_M_HenchmanTough',
            variants=['0|3'],
            enlightenment=(2, 180)
        )

        await ctx.send(f'Skin set to Golden Brutus.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to Golden Meowscles "
                    "(shortcut for !enlightened CID_693_Athena_Commando_M_BuffCat 2 220).",
        help="Sets the outfit of the client to Golden Meowscles.\n"
             "Example: !goldenmeowscles",
        usage="!goldenmeowscles"
    )
    async def goldenmeowscles(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_693_Athena_Commando_M_BuffCat',
            variants=['0|3'],
            enlightenment=(2, 220)
        )

        await ctx.send(f'Skin set to Golden Meowscles.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to Golden Midas "
                    "(shortcut for !enlightened CID_694_Athena_Commando_M_CatBurglar 2 140).",
        help="Sets the outfit of the client to Golden Peely.\n"
             "Example: !goldenmidas",
        usage="!goldenmidas"
    )
    async def goldenmidas(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_694_Athena_Commando_M_CatBurglar',
            variants=['0|3'],
            enlightenment=(2, 140)
        )

        await ctx.send(f'Skin set to Golden Midas.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to Golden Skye "
                    "(shortcut for !enlightened CID_690_Athena_Commando_F_Photographer 2 300).",
        help="Sets the outfit of the client to Golden Skye.\n"
             "Example: !goldenskye",
        usage="!goldenskye"
    )
    async def goldenskye(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_690_Athena_Commando_F_Photographer',
            variants=['0|3'],
            enlightenment=(2, 350)
        )

        await ctx.send(f'Skin set to Golden Skye.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Sets the outfit of the client to Golden TNTina "
                    "(shortcut for !enlightened CID_691_Athena_Commando_F_TNTina 2 350).",
        help="Sets the outfit of the client to Golden TNTina.\n"
             "Example: !goldentntina",
        usage="!goldentntina"
    )
    async def goldentntina(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_outfit(
            asset='CID_691_Athena_Commando_F_TNTina',
            variants=['0|3'],
            enlightenment=(2, 260)
        )

        await ctx.send(f'Skin set to Golden TNTina.')

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Equips a To-Be-Determined outfit.",
        help="Equips a To-Be-Determined outfit.\n"
             "Example: !tbd 2"
    )
    async def tbd(self, ctx: rebootpy.ext.commands.Context, skin: int = 1) -> None:
        cosmetics = await self.bot.fortnite_api.cosmetics.get_cosmetics(
            matchMethod="full",
            name="TBD",
            backendType="AthenaCharacter"
        )

        if not skin or skin > len(cosmetics):
            return await ctx.send(f'Invalid skin number, there is only {len(cosmetics)} TBD outfits.')

        await ctx.send(f'Found {len(cosmetics)} TBD outfits.')

        await self.bot.party.me.set_outfit(asset=cosmetics[skin - 1].id)

        await ctx.send(f'Skin set to {cosmetics[skin - 1].id}\nUse !tbd <1 to {len(cosmetics)}> to equip another.')
        print(self.bot.message % f"Set skin to: {cosmetics[skin - 1].id}.")

    @commands.dm_only()
    @commands.command(
        description="[Cosmetic] Plays the Dab Stand emote, primarily used to"
                    "show of your back bling.",
        help="Plays the Dab Stand emote, "
             "primarily used to show of your back bling.\n"
             "Example: !dabstand",
        usage="!dabstand"
    )
    async def dabstand(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_emote(
            asset='EID_HandstandLegDab'
        )

        await ctx.send('Emote set to Dab Stand!')
        print(self.bot.message % f"Emote set to Dab Stand.")
