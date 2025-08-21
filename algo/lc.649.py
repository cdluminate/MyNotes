class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        senates = list(senate)
        while len(set(senates)) > 1:
            #print('>', senates)
            current = senates[0]
            enemy_idx = senates.index('R' if current == 'D' else 'D')
            senates.pop(enemy_idx)
            senates.pop(0)
            senates.append(current)
        if senates[0] == 'R':
            return 'Radiant'
        else:
            return 'Dire'
