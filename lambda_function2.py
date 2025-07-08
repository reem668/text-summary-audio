import boto3
import os
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
comprehend = boto3.client('comprehend')
polly = boto3.client('polly')

def summarize_text(text):
    response = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
    phrases = sorted(response['KeyPhrases'], key=lambda x: x['Score'], reverse=True)
    summary = ' '.join([p['Text'] for p in phrases[:5]])
    return summary

def lambda_handler(event, context):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = unquote_plus(record['s3']['object']['key'])

    if not key.startswith("input/"):
        return {"message": "Invalid prefix"}

    # Read original text
    obj = s3.get_object(Bucket=bucket, Key=key)
    text = obj['Body'].read().decode('utf-8')

    # Generate summary
    summary = summarize_text(text)

    # Save summary text
    summary_key = f"output/summary-{os.path.basename(key)}"
    s3.put_object(Bucket=bucket, Key=summary_key, Body=summary.encode('utf-8'))

    # Generate speech using Polly
    speech = polly.synthesize_speech(Text=summary, OutputFormat='mp3', VoiceId='Joanna')
    audio_key = f"audio/audio-{os.path.splitext(os.path.basename(key))[0]}.mp3"
    s3.put_object(Bucket=bucket, Key=audio_key, Body=speech['AudioStream'].read(), ContentType='audio/mpeg')

    return {
        "summary_file": summary_key,
        "audio_file": audio_key
    }