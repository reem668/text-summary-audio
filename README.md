
# 🎧 Text Summary to Audio using AWS Lambda

This project:
- Takes a `.txt` file uploaded to S3
- Uses AWS Comprehend to extract key phrases
- Uses Polly to convert them to audio
- Stores the result in `output/` and `audio/` folders in S3

## AWS Services Used
- S3 (input/, output/, audio/)
- Lambda (Python)
- Comprehend
- Polly

## How to Use
1. Upload `.txt` to S3 `input/` folder
2. Lambda triggers
3. Result:
   - Summary text in `output/`
   - Audio (.mp3) in `audio/`

## IAM Role Requirements
- AmazonS3FullAccess
- AmazonComprehendFullAccess
- AmazonPollyFullAccess

