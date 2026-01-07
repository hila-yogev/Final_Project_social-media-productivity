from social_media_productivity.pipeline import run_pipeline

def main():
    df = run_pipeline()
    print(df.shape)

if __name__ == "__main__":
    main()
