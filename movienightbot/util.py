import datetime
from typing import List
import asyncio
import logging

import discord

from .db.controllers import ServerController, MovieVoteController, MovieVote
from imdb import IMDb


logger = logging.getLogger("movienightbot")


async def cleanup_messages(
    messages: List[discord.Message], sec_delay: int = 10
) -> None:
    """Deletes a list of messages off a server

    Parameters
    ----------
    messages : List of doscord.Message objects
        The messages to delete
    sec_delay : int
        The number of seconds to wait before deleting the message. Default 10
    """
    loop = asyncio.get_event_loop()
    for message in messages:
        loop.create_task(message.delete(delay=sec_delay))
        # Need sleep here so don't overwhelm API
        await asyncio.sleep(0.25)


def build_vote_embed(server_id: int):
    server_row = ServerController().get_by_id(server_id)
    movie_rows = MovieVoteController().get_movies_for_server_vote(server_id)
    embed = discord.Embed(
        title="Movie Vote!",
        description=f"""Use the emojis to vote on your preferred movies, in the order you would prefer them.
You may vote for up to {server_row.num_votes_per_user} movies.
Reset your votes with the :arrows_counterclockwise: emoji.
End the vote with the :octagonal_sign: emoji.""",
    )
    for movie_vote in movie_rows:
        movie = movie_vote.movie
        imdb_info = movie.imdb_id
        movie_info = f"{movie_vote.emoji} {movie.movie_name}"
        score = f"Score: {movie_vote.score:.2f}"
        if imdb_info:
            movie_info += f" ({imdb_info.year})"
            score += (
                f" - [IMDb Page](https://www.imdb.com/title/tt{imdb_info.imdb_id}/)"
            )

        embed.add_field(
            name=movie_info, value=score, inline=False,
        )
    embed.set_footer(text="Movie time is")
    today = datetime.datetime.utcnow().date()
    movie_hour, movie_minute = server_row.movie_time.split(":")
    movie_time = datetime.datetime(
        year=today.year,
        month=today.month,
        day=today.day,
        hour=int(movie_hour),
        minute=int(movie_minute),
        tzinfo=datetime.timezone.utc,
    )
    embed.timestamp = movie_time
    return embed


emojis_text = {
    ":regional_indicator_a:": "🇦",
    ":regional_indicator_b:": "🇧",
    ":regional_indicator_c:": "🇨",
    ":regional_indicator_d:": "🇩",
    ":regional_indicator_e:": "🇪",
    ":regional_indicator_f:": "🇫",
    ":regional_indicator_g:": "🇬",
    ":regional_indicator_h:": "🇭",
    ":regional_indicator_i:": "🇮",
    ":regional_indicator_j:": "🇯",
    ":regional_indicator_k:": "🇰",
    ":regional_indicator_l:": "🇱",
    ":regional_indicator_m:": "🇲",
    ":regional_indicator_n:": "🇳",
    ":regional_indicator_o:": "🇴",
    ":regional_indicator_p:": "🇵",
    ":regional_indicator_q:": "🇶",
    ":regional_indicator_r:": "🇷",
    ":regional_indicator_s:": "🇸",
    ":regional_indicator_t:": "🇹",
    ":regional_indicator_u:": "🇺",
    ":regional_indicator_v:": "🇻",
    ":regional_indicator_w:": "🇼",
    ":regional_indicator_x:": "🇽",
    ":regional_indicator_y:": "🇾",
    ":regional_indicator_z:": "🇿",
    ":octagonal_sign:": "🛑",
    ":arrows_counterclockwise:": "🔄",
}


emojis_unicode = {v: k for k, v in emojis_text.items()}


async def add_vote_emojis(vote_msg: discord.Message, movie_votes: MovieVote):
    for movie_vote in movie_votes:
        await vote_msg.add_reaction(emojis_text[movie_vote.emoji])
    await vote_msg.add_reaction(emojis_text[":arrows_counterclockwise:"])


def get_imdb_info(movie_name: str, kind: str = "movie"):
    if not movie_name:
        return None

    im_db = IMDb()
    results = im_db.search_movie(movie_name)
    logger.debug("IMDB RESULTS: " + str(results))
    for r in results:
        if kind not in r.get("kind", ""):
            logger.debug(str(r) + " is not movie, skipping")
            continue
        if r["title"].lower() == movie_name.lower():
            logger.debug(movie_name + "  Matched  " + str(r))
            return r
    logger.debug(movie_name + "  Unmatched")
    return None
