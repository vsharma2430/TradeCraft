with open('commands\pip.txt', 'r') as f:
    print(' && '.join([line.strip() for line in f.readlines()]))
    
'''
pip install yfinance && pip install jugaad-data && pip install nselib && pip install PyQt5 && pip install matplotlib && pip3 install sklearn-model && pip install rocketry && pip install fastapi && pip install uvicorn
'''