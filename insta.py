import instaloader

L = instaloader.Instaloader(download_pictures=False,
                            download_videos=False, 
                            download_video_thumbnails=False,
                            compress_json=False, 
                            download_geotags=False, 
                            post_metadata_txt_pattern="", 
                            max_connection_attempts=0,
                            download_comments=False)

L.download_delay = 10  # or higher if needed

def get_followers(target_account):
    print("fetching followers", flush=True)
    i=0
    followers = []
    profile = instaloader.Profile.from_username(L.context, target_account)
    for follower in profile.get_followers():
        followers.append(follower.username)
        i+=1
        if i%100==0:
            print(f"{i}th follower:", follower.username, flush=True)

    with open(f"{target_account}_followers.txt", 'w') as f:
        for follower in followers:
            f.write(follower+'\n')
        f.close()

def get_following(target_account):
    print("fetching following", flush=True)
    i=0
    following = []
    profile = instaloader.Profile.from_username(L.context, target_account)
    for followee in profile.get_followees():
        following.append(followee.username)
        i+=1
        if i%100==0:
            print(f"{i}th following:", followee.username, flush=True)

    with open(f"{target_account}_following.txt", 'w') as f:
        for followee in following:
            f.write(followee+'\n')
        f.close()

def get_not_following_back(target_account):
    with open(f"{target_account}_followers.txt", 'r') as f:
        followers = {line.strip() for line in f}
    with open(f"{target_account}_following.txt", 'r') as f:
        following = {line.strip() for line in f}

    not_following_back = following - followers

    with open(f'{target_account}_not_following_back.txt', 'w') as f:
        for user in not_following_back:
            f.write(user+'\n')
        f.close()

    filtered_users = []

    i = 0

    for user in not_following_back:
        profile = instaloader.Profile.from_username(L.context, user)
        if profile.is_private and profile.followers < 10000:
            filtered_users.append(user)
        i += 1
        if i%10==0:
            print(f"checking {i}th user:", user, flush=True)

    # Write filtered users to a file
    with open(f'{target_account}_not_following_back_filtered.txt', 'w') as f:
        for user in filtered_users:
            f.write(user+'\n')
        f.close()

if __name__ == "__main__":
    temp_username = "older.lee12345"
    temp_password = "Fuckyou.com123"
    my_username = "jwooziee"

    L.login(temp_username, temp_password)
    # get_followers(my_username)
    # get_following(my_username)
    get_not_following_back(my_username)