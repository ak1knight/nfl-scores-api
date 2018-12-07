from bs4 import BeautifulSoup
import urllib.request
import json

def get_team_data_for_id(team_id):
    data = {}
    with urllib.request.urlopen('https://www.pro-football-reference.com/teams/' + str(team_id) + '/2018/gamelog/') as response:
        soup = BeautifulSoup(response.read().decode('utf-8'), 'html.parser')

        title = str(soup.title.text)
        data['name'] = title[:title.index('2018') - 1]
        data['logo_url'] = soup.find(attrs={'class': 'teamlogo'})['src']
        data['games'] = []
        for row in soup.find(id='gamelog2018').find_all('tr'):
            if row.find(attrs={"data-stat": "week_num", "scope": "row"}) is not None:
                game = {}
                game['week'] = row.find(attrs={"data-stat": "week_num"}).text
                game['game_date'] = row.find(attrs={"data-stat": "game_date"})['csk']
                game['outcome'] = row.find(attrs={"data-stat": "game_outcome"}).text
                game['opponent'] = row.find(attrs={"data-stat": "opp"}).text
                game['team_points'] = row.find(attrs={"data-stat": "pts_off"}).text
                game['opp_points'] = row.find(attrs={"data-stat": "pts_def"}).text
                data['games'].append(game)
        
        return data

def handler(event, context):
    data = get_team_data_for_id(event['pathParameters']['team_id'])
    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {'Content-Type': 'application/json'}
    }