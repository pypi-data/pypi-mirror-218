from setuptools import setup

if __name__ == '__main__':
    setup(
        package_data={'illini_snake': 
        [ 
            'static/opponent_logos/*.png',
            'static/opponent_logos/*.svg',
            'static/Illinois.png',
            'static/nom nom nom.wav',
            'settings.json'
        ]
        }
    )