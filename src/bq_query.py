top_dates_with_top_users = r"""
    WITH
    TopDates AS (
        SELECT
            CAST(date AS DATE) AS tweets_date,
            COUNT(id) AS tweet_count
        FROM latam_tweets_dataset.tweets
        WHERE id IS NOT NULL
        GROUP BY tweets_date
        ORDER BY tweet_count DESC
        LIMIT 10
    ),
    TopUsersDate AS (
        SELECT
            TD.tweets_date,
            TW.user.username,
            MAX(TD.tweet_count) AS max_tweet_count,
            COUNT(TW.id) AS user_tweet_count,
            ROW_NUMBER() OVER (
                PARTITION BY TD.tweets_date
                ORDER BY MAX(TD.tweet_count) DESC, COUNT(*) DESC
            ) AS row_number
        FROM latam_tweets_dataset.tweets AS TW
        INNER JOIN TopDates AS TD
            ON TD.tweets_date = CAST(TW.date AS DATE)
        WHERE TW.id IS NOT NULL
        GROUP BY
            TD.tweets_date,
            TW.user.username
        ORDER BY
            max_tweet_count DESC,
            user_tweet_count DESC,
            TW.user.username ASC
    )

    SELECT
        tweets_date,
        username
    FROM TopUsersDate
    WHERE row_number = 1
"""

"""
Top 10 most used emojis with their respective counts.
Assumption: The query does not contain duplicate entries, as the tweet with 'id = 1362813218952007687' contains two heart and two fist emojis.
Assumption: A valid tweet has an id
"""
top_emojis = r"""
    WITH
    ExtractedEmojis AS (
        SELECT
            REGEXP_EXTRACT_ALL(
                content,
                FORMAT(
                    r"(?:[\x{1F300}-\x{1F5FF}]|[\x{1F900}-\x{1F9FF}]|[\x{1F600}-\x{1F64F}]|[\x{1F680}-\x{1F6FF}]" ||
                    r"|[\x{2600}-\x{26FF}]\x{FE0F}?|[\x{2700}-\x{27BF}]\x{FE0F}?|\x{24C2}\x{FE0F}?|[\x{1F1E6}-\x{1F1FF}]{1,2}" ||
                    r"|[\x{1F170}\x{1F171}\x{1F17E}\x{1F17F}\x{1F18E}\x{1F191}-\x{1F19A}]\x{FE0F}?" ||
                    r"|[\\x{0023}\x{002A}\x{0030}-\x{0039}]\x{FE0F}?\x{20E3}|[\x{2194}-\x{2199}\x{21A9}-\x{21AA}]\x{FE0F}?" ||
                    r"|[\x{2B05}-\x{2B07}\x{2B1B}\x{2B1C}\x{2B50}\x{2B55}]\x{FE0F}?|[\x{2934}\x{2935}]\x{FE0F}?" ||
                    r"|[\x{3297}\x{3299}]\x{FE0F}?|[\x{1F201}\x{1F202}\x{1F21A}\x{1F22F}\x{1F232}\x{1F23A}\x{1F250}\x{1F251}]\x{FE0F}?" ||
                    r"|[\x{203C}-\x{2049}]\x{FE0F}?|[\x{00A9}-\x{00AE}]\x{FE0F}?|[\x{2122}\x{2139}]\x{FE0F}?" ||
                    r"|\x{1F004}\x{FE0F}?|\x{1F0CF}\x{FE0F}?|[\x{231A}\x{231B}\x{2328}\x{23CF}\x{23E9}\x{23F3}\x{23F8}\x{23FA}]\x{FE0F}?)"
                )
            ) AS emojis
        FROM latam_tweets_dataset.tweets
        WHERE id IS NOT NULL
    )

    SELECT
        emoji,
        COUNT(emoji) AS count
    FROM ExtractedEmojis
    CROSS JOIN UNNEST(emojis) AS emoji
    GROUP BY emoji
    ORDER BY count DESC
    LIMIT 10
"""

"""
Top 10 all-time most influential users (username) based on the count of mentions (@) each of them receives.
Assumption: A valid tweet has an id
"""
top_influential_users = r"""
    WITH
    MentionedUsersCount AS (
        SELECT
            user.username AS username,
            COUNT(user.username) AS count
        FROM
            latam_tweets_dataset.tweets as TW,
            UNNEST(mentionedUsers) AS user
        WHERE TW.id IS NOT NULL
        GROUP BY username
    )

    SELECT
        username,
        count AS mention_count
    FROM MentionedUsersCount
    ORDER BY count DESC
    LIMIT 10
"""