#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import re
import requests
from urllib.parse import quote

os.system('clear' if os.name == 'posix' else 'cls')

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
WHITE = '\033[97m'
MAGENTA = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'

BANNER = f"""
{RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠚⣷⠀⠀⣀⣤⠀⠀⠀⠀⠀⠀⠀{RESET}
{RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⣟⢀⡴⠋⠀⠀⣿⠖⠋⢀⡏⠀⠀⠀⡀⡀⠀⠀{RESET}
{RED}⠀⠀⠀⠀⠀⠀⠀⢀⡀⡼⠀⢸⡟⡸⠀⠀⠀⠃⠀⠀⢸⡧⠜⠛⠛⣻⠃⠀⠀{RESET}
{RED}⠀⠀⠀⠀⠀⠀⠀⢺⢾⡃⠀⠈⣴⠁⢻⡀⠀⠀⢀⡠⠀⠀⠀⠀⢸⣇⣤⡀⠀{RESET}
{RED}⠀⠀⠀⠀⠀⠀⠀⠸⡜⠂⠀⠀⣟⠀⢸⠑⠀⠰⠁⠀⠀⠀⠀⠀⠛⠉⡼⠁⠀{RESET}
{RED}⠀⠀⠀⠀⠀⠀⠀⠈⣷⣾⣿⣿⣿⣿⣾⣶⣶⣤⣀⡀⢰⠕⠋⠀⠀⠸⠧⣤⡄{RESET}
{RED}⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣔⠈⣤⣶⡚⠁⠀{RESET}
{RED}⠀⠀⠀⠀⣠⣶⡀⢸⡟⠿⡿⠿⡟⠻⠿⣿⣿⣿⣿⣿⣿⣿⠿⣿⠋⠁⠀⠀⠀{RESET}
{RED}⠀⠀⠀⢰⢧⡷⡿⢘⡎⠀⠀⠐⣶⢶⣲⠈⠙⠋⠉⠉⠁⡘⡯⣿⡶⣆⡀⠀⠀{RESET}
{RED}⠀⠀⠀⢾⢈⣼⣿⣤⣿⣶⣶⣶⣿⣿⣧⣤⣄⣀⣀⣤⣾⣿⣿⢯⢇⣿⢳⠀⠀{RESET}
{RED}⠀⠀⠀⠈⠙⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⣷⣬⠏⠀⠀{RESET}
{RED}⠀⠀⠀⠀⠀⠀⠀⠉⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠻⠟⠋⠁⠀⠀⠀{RESET}
{RED}⠀⠀⠀⠀⢀⣀⣀⡀⣰⣿⣿⣿⣿⣿⣿⣿⡿⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{RESET}
{RED}⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{RESET}
{RED}⠀⠀⠀⠀⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{RESET}
{RED}⢀⣤⣶⣴⣿⣿⣿⡧⠀⠉⠙⢿⣿⣿⣿⣿⣾⣶⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀{RESET}
{RED}⠀⠉⠛⠛⠿⣿⣿⡇⠀⠀⠀⠀⠻⣿⣿⣿⡿⠿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀{RESET}
{RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠸⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀{RESET}
{RED}
{RED}   ╔══════════════════════════════════════════════════════════════════╗
{RED}   ║{CYAN}                      TIKTOK OSINT TOOL                           {RED}║
{RED}   ║{YELLOW}                    CREATOR: AnsXploit                            {RED}║
{RED}   ╚══════════════════════════════════════════════════════════════════╝{RESET}
"""

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
}

class TikTokOSINT:
    def __init__(self, username):
        self.username = username.replace('@', '')
        self.data = {}
        
    def get_user_info(self):
        try:
            url = f"https://www.tiktok.com/@{self.username}"
            response = requests.get(url, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                
                uid_match = re.search(r'"id":"([0-9]+)"', html)
                if uid_match:
                    self.data['user_id'] = uid_match.group(1)
                
                unique_id_match = re.search(r'"uniqueId":"([^"]+)"', html)
                if unique_id_match:
                    self.data['username'] = unique_id_match.group(1)
                
                nickname_match = re.search(r'"nickname":"([^"]+)"', html)
                if nickname_match:
                    self.data['nickname'] = nickname_match.group(1)
                
                bio_match = re.search(r'"bioDescription":"([^"]+)"', html)
                if bio_match:
                    self.data['bio'] = bio_match.group(1)
                
                follower_match = re.search(r'"followerCount":([0-9]+)', html)
                if follower_match:
                    self.data['followers'] = int(follower_match.group(1))
                
                following_match = re.search(r'"followingCount":([0-9]+)', html)
                if following_match:
                    self.data['following'] = int(following_match.group(1))
                
                heart_match = re.search(r'"heartCount":([0-9]+)', html)
                if heart_match:
                    self.data['total_likes'] = int(heart_match.group(1))
                
                video_match = re.search(r'"videoCount":([0-9]+)', html)
                if video_match:
                    self.data['videos'] = int(video_match.group(1))
                
                verified_match = re.search(r'"verified":(true|false)', html)
                if verified_match:
                    self.data['verified'] = verified_match.group(1) == 'true'
                
                private_match = re.search(r'"privateAccount":(true|false)', html)
                if private_match:
                    self.data['private_account'] = private_match.group(1) == 'true'
                
                avatar_match = re.search(r'"avatarLarger":"([^"]+)"', html)
                if avatar_match:
                    self.data['avatar_url'] = avatar_match.group(1).replace('\\u002F', '/')
                
                signature_match = re.search(r'"signature":"([^"]+)"', html)
                if signature_match:
                    self.data['signature'] = signature_match.group(1)
                
                region_match = re.search(r'"region":"([^"]+)"', html)
                if region_match:
                    self.data['region'] = region_match.group(1)
                
                language_match = re.search(r'"language":"([^"]+)"', html)
                if language_match:
                    self.data['language'] = language_match.group(1)
                
                create_time_match = re.search(r'"createTime":([0-9]+)', html)
                if create_time_match:
                    import datetime
                    self.data['account_created'] = datetime.datetime.fromtimestamp(int(create_time_match.group(1))).strftime('%Y-%m-%d %H:%M:%S')
                
                sec_uid_match = re.search(r'"secUid":"([^"]+)"', html)
                if sec_uid_match:
                    self.data['sec_uid'] = sec_uid_match.group(1)
                
                return True
        except Exception as e:
            self.data['error'] = str(e)
        return False
    
    def get_user_videos(self):
        try:
            user_id = self.data.get('user_id', '')
            if user_id:
                api_url = f"https://www.tiktok.com/api/post/item_list/?aid=1988&count=30&cursor=0&user_id={user_id}"
                response = requests.get(api_url, headers=HEADERS, timeout=15)
                if response.status_code == 200:
                    videos = response.json()
                    if 'itemList' in videos:
                        self.data['recent_videos'] = []
                        for video in videos['itemList'][:10]:
                            vid_data = {
                                'video_id': video.get('id', ''),
                                'description': video.get('desc', ''),
                                'play_count': video.get('stats', {}).get('playCount', 0),
                                'like_count': video.get('stats', {}).get('diggCount', 0),
                                'comment_count': video.get('stats', {}).get('commentCount', 0),
                                'share_count': video.get('stats', {}).get('shareCount', 0),
                                'duration': video.get('video', {}).get('duration', 0),
                                'create_time': video.get('createTime', 0)
                            }
                            self.data['recent_videos'].append(vid_data)
        except:
            pass
    
    def check_social_links(self):
        try:
            url = f"https://www.tiktok.com/@{self.username}"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 200:
                bio_links = re.findall(r'(https?://[^\s"\'>]+)', response.text)
                self.data['external_links'] = list(set(bio_links))[:5]
        except:
            self.data['external_links'] = []
    
    def get_user_followers_info(self):
        try:
            user_id = self.data.get('user_id', '')
            if user_id:
                api_url = f"https://www.tiktok.com/api/follower/list/?aid=1988&count=10&user_id={user_id}&cursor=0"
                response = requests.get(api_url, headers=HEADERS, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if 'followers' in data:
                        self.data['sample_followers'] = []
                        for follower in data['followers'][:5]:
                            self.data['sample_followers'].append({
                                'username': follower.get('uniqueId', ''),
                                'user_id': follower.get('userId', ''),
                                'nickname': follower.get('nickname', '')
                            })
        except:
            pass
    
    def display_results(self):
        print(f"\n{CYAN}╔══════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{CYAN}║{WHITE}                    TIKTOK OSINT RESULT                           {CYAN}║{RESET}")
        print(f"{CYAN}╚══════════════════════════════════════════════════════════════════╝{RESET}")
        
        print(f"\n{GREEN}[ ACCOUNT INFORMATION ]{RESET}")
        print(f"{YELLOW}├─ Username      : {WHITE}@{self.data.get('username', 'N/A')}{RESET}")
        print(f"{YELLOW}├─ User ID       : {WHITE}{self.data.get('user_id', 'N/A')}{RESET}")
        print(f"{YELLOW}├─ Sec UID       : {WHITE}{self.data.get('sec_uid', 'N/A')}{RESET}")
        print(f"{YELLOW}├─ Nickname      : {WHITE}{self.data.get('nickname', 'N/A')}{RESET}")
        print(f"{YELLOW}├─ Bio           : {WHITE}{self.data.get('bio', 'N/A')}{RESET}")
        print(f"{YELLOW}├─ Signature     : {WHITE}{self.data.get('signature', 'N/A')}{RESET}")
        print(f"{YELLOW}├─ Verified      : {WHITE}{'✓ Yes' if self.data.get('verified') else '✗ No'}{RESET}")
        print(f"{YELLOW}├─ Private       : {WHITE}{'✓ Yes' if self.data.get('private_account') else '✗ No'}{RESET}")
        print(f"{YELLOW}├─ Region        : {WHITE}{self.data.get('region', 'N/A')}{RESET}")
        print(f"{YELLOW}├─ Language      : {WHITE}{self.data.get('language', 'N/A')}{RESET}")
        print(f"{YELLOW}├─ Created       : {WHITE}{self.data.get('account_created', 'N/A')}{RESET}")
        print(f"{YELLOW}└─ Avatar URL    : {WHITE}{self.data.get('avatar_url', 'N/A')[:80]}{'...' if len(self.data.get('avatar_url', '')) > 80 else ''}{RESET}")
        
        print(f"\n{GREEN}[ STATISTICS ]{RESET}")
        print(f"{YELLOW}├─ Followers     : {WHITE}{self.data.get('followers', 0):,}{RESET}")
        print(f"{YELLOW}├─ Following     : {WHITE}{self.data.get('following', 0):,}{RESET}")
        print(f"{YELLOW}├─ Total Likes   : {WHITE}{self.data.get('total_likes', 0):,}{RESET}")
        print(f"{YELLOW}└─ Total Videos  : {WHITE}{self.data.get('videos', 0):,}{RESET}")
        
        if self.data.get('external_links'):
            print(f"\n{GREEN}[ EXTERNAL LINKS ]{RESET}")
            for i, link in enumerate(self.data['external_links'], 1):
                print(f"{YELLOW}├─ [{i}] {WHITE}{link}{RESET}")
        
        if self.data.get('recent_videos'):
            print(f"\n{GREEN}[ RECENT VIDEOS (5 Terbaru) ]{RESET}")
            for i, video in enumerate(self.data['recent_videos'][:5], 1):
                print(f"{YELLOW}├─ Video {i}:{RESET}")
                print(f"{YELLOW}│  ├─ ID         : {WHITE}{video['video_id']}{RESET}")
                print(f"{YELLOW}│  ├─ URL        : {WHITE}https://www.tiktok.com/@user/video/{video['video_id']}{RESET}")
                print(f"{YELLOW}│  ├─ Desc       : {WHITE}{video['description'][:60]}{'...' if len(video['description']) > 60 else ''}{RESET}")
                print(f"{YELLOW}│  ├─ Plays      : {WHITE}{video['play_count']:,}{RESET}")
                print(f"{YELLOW}│  ├─ Likes      : {WHITE}{video['like_count']:,}{RESET}")
                print(f"{YELLOW}│  ├─ Comments   : {WHITE}{video['comment_count']:,}{RESET}")
                print(f"{YELLOW}│  └─ Shares     : {WHITE}{video['share_count']:,}{RESET}")
        
        if self.data.get('sample_followers'):
            print(f"\n{GREEN}[ SAMPLE FOLLOWERS (5 Akun) ]{RESET}")
            for i, follower in enumerate(self.data['sample_followers'][:5], 1):
                print(f"{YELLOW}├─ [{i}] {WHITE}@{follower['username']} (ID: {follower['user_id']}){RESET}")
        
        print(f"\n{CYAN}══════════════════════════════════════════════════════════════════{RESET}")
        
        with open(f"tiktok_{self.username}_full.json", 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
        print(f"{GREEN}[✓] Full data saved to: tiktok_{self.username}_full.json{RESET}")
        
        print(f"\n{YELLOW}[!] Profile URL     : https://www.tiktok.com/@{self.username}{RESET}")
        if self.data.get('user_id'):
            print(f"{YELLOW}[!] User ID          : {self.data['user_id']}{RESET}")
            print(f"{YELLOW}[!] API Embed URL    : https://www.tiktok.com/@?refer=embed&user_id={self.data['user_id']}{RESET}")

def main():
    print(BANNER)
    
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input(f"{BOLD}{GREEN}[TIKTOK OSINT]{RESET} Masukkan username: ").strip()
    
    username = username.replace('@', '')
    
    print(f"\n{YELLOW}[*] Scanning TikTok user: @{username}{RESET}")
    print(f"{YELLOW}[*] Gathering full data...{RESET}\n")
    
    osint = TikTokOSINT(username)
    
    if osint.get_user_info():
        osint.get_user_videos()
        osint.check_social_links()
        osint.get_user_followers_info()
        osint.display_results()
    else:
        print(f"\n{RED}[!] User not found or private account!{RESET}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Interrupted{RESET}")
        sys.exit(0)