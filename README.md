# Machine Learning Streaming Pipeline using DataFlow (under construction)
This is one of the **Introduction to Apache Beam using Python** Repository. Here we will try to learn basics of Apache Beam to create **Streaming** pipelines. We will learn step by step how to create a streaming pipeline using [German Credit Risk](https://www.kaggle.com/uciml/german-credit). The complete process is divided into 8 parts:

1. **Generating Streaming Data**
2. **Reading Data from Pub Sub**
3. **Parsing the data**
4. **Filtering the data**
5. **Performing Type Convertion**
6. **Data wrangling**
7. **Deleting Unwanted Columns**
8. **Inserting Data in Bigquery**


## Motivation
For the last two years, I have been part of a great learning curve wherein I have upskilled myself to move into a Machine Learning and Cloud Computing. This project was practice project for all the learnings I have had. This is first of the many more to come. 
 

## Libraries/frameworks used

<b>Built with</b>
- [Apache Beam](https://beam.apache.org/documentation/programming-guide/)
- [Anaconda](https://www.anaconda.com/)
- [Python](https://www.python.org/)
- [Google DataFlow](https://cloud.google.com/dataflow)
- [Google Cloud Storage](https://cloud.google.com/storage)
- [Google Bigquery](https://cloud.google.com/bigquery)
- [Google Pub/Sub](https://cloud.google.com/pubsub)

## Cloning Repository

```bash
    # clone this repo:
    git clone https://github.com/adityasolanki205/ML-Streaming-pipeline-using-Dataflow.git
```

## Pipeline Construction

Below are the steps to setup the enviroment and run the codes:

1. **Setup**: First we will have to setup free google cloud account which can be done [here](https://cloud.google.com/free). Then we need to Download the data from [German Credit Risk](https://www.kaggle.com/uciml/german-credit).

2. **Cloning the Repository to Cloud SDK**: We will have to copy the repository on Cloud SDK using below command:

```bash
    # clone this repo:
    git clone https://github.com/adityasolanki205/ML-Streaming-pipeline-using-Dataflow.git
```

3. **Generating Streaming Data**: We need to generate streaming data that can be published to Pub Sub. Then those messages will be picked to be processed by the pipeline. To generate data we will use **random()** library to create input messages. Using the generating_data.py we will be able to generate random data in the required format. This generated data will be published to Pub/Sub using publish_to_pubsub.py. Here we will use PublisherClient object, add the path to the topic using the topic_path method and call the publish_to_pubsub() function while passing the topic_path and data.

```python
    import random

    LINE ="""   {Existing_account} 
                {Duration_month} 
                {Credit_history} 
                {Purpose} 
                {Credit_amount} 
                .....
                {Classification}"""

    def generate_log():
        existing_account = ['B11','A12','C14',
                            'D11','E11','A14',
                            'G12','F12','A11',
                            'H11','I11',
                            'J14','K14','L11',
                            'A13'
                           ]
        Existing_account = random.choice(existing_account)
    
        duration_month = []
        for i  in range(6, 90 , 3):
            duration_month.append(i)
        Duration_month = random.choice(duration_month)
        ....
        foreign_worker = ['A201',
                        'A202']
        Foreign_worker = random.choice(foreign_worker)
        log_line = LINE.format(
            Existing_account=Existing_account,
            Duration_month=Duration_month,
            Credit_history=Credit_history,
            Purpose=Purpose,
            ...
            Foreign_worker=Foreign_worker
        )

        return log_line

```

4. **Reading Data from Pub Sub**: Now we will start reading data from Pub sub to start the pipeline . The data is read using **beam.io.ReadFromPubSub()**. Here we will just read the input message by providing the TOPIC and the output is decoded which was encoded while generating the data. 

```python
    def run(argv=None, save_main_session=True):
        parser = argparse.ArgumentParser()
        parser.add_argument(
          '--input',
          dest='input',
          help='Input file to process')
        parser.add_argument(
          '--output',
          dest='output',
          default='../output/result.txt',
          help='Output file to write results to.')
        known_args, pipeline_args = parser.parse_known_args(argv)
        options = PipelineOptions(pipeline_args)
        TOPIC ="projects/trusty-field-283517/topics/german_credit_data"
        with beam.Pipeline(options=PipelineOptions()) as p:
            encoded_data = ( p 
                             | 'Read data' >> beam.io.ReadFromPubSub(topic=TOPIC).with_output_types(bytes) 
                           )
                    data = ( encoded_data
                             | 'Decode' >> beam.Map(lambda x: x.decode('utf-8') ) 
                           ) 
    if __name__ == '__main__':
        run()
``` 

5. **Parsing the data**: After reading the input from Pub-Sub we will split the data using split(). Data is segregated into different columns to be used in further steps. We will **ParDo()** to create a split function. The output of this step is present in SplitPardo text file.

```python
    class Split(beam.DoFn):
        #This Function Splits the Dataset into a dictionary
        def process(self, element): 
            Existing_account,
            Duration_month,
            Credit_history,
            Purpose,
            Credit_amount,
            Saving,
            Employment_duration,
            Installment_rate,
            Personal_status,
            Debtors,
            Residential_Duration,
            Property,
            Age,
            Installment_plans,
            Housing,
            Number_of_credits
            Job,
            Liable_People,
            Telephone,
            Foreign_worker= element.split(' ')
        return [{
            'Existing_account': str(Existing_account),
            'Duration_month': str(Duration_month),
            'Credit_history': str(Credit_history),
            'Purpose': str(Purpose),
            'Credit_amount': str(Credit_amount),
            'Saving': str(Saving),
            'Employment_duration':str(Employment_duration),
            'Installment_rate': str(Installment_rate),
            'Personal_status': str(Personal_status),
            'Debtors': str(Debtors),
            'Residential_Duration': str(Residential_Duration),
            'Property': str(Property),
            'Age': str(Age),
            'Installment_plans':str(Installment_plans),
            'Housing': str(Housing),
            'Number_of_credits': str(Number_of_credits),
            'Job': str(Job),
            'Liable_People': str(Liable_People),
            'Telephone': str(Telephone),
            'Foreign_worker': str(Foreign_worker)
        }]
    def run(argv=None, save_main_session=True):
        ...
        with beam.Pipeline(options=PipelineOptions()) as p:
            encoded_data = ( p 
                             | 'Read data' >> beam.io.ReadFromPubSub(topic=TOPIC).with_output_types(bytes))
                    data = ( encoded_data
                             | 'Decode' >> beam.Map(lambda x: x.decode('utf-8')))  
            parsed_data  = (  data 
                             | 'Parsing Data' >> beam.ParDo(Split())
                             | 'Writing output' >> beam.io.WriteToText(known_args.output)
                           )

    if __name__ == '__main__':
        run()
``` 

6. **Performing Type Convertion**: After Filtering we will convert the datatype of numeric columns from String to Int or Float datatype. Here we will use **Map()** to apply the Convert_Datatype(). The output of this step is saved in Converted_datatype text file.

```python
    ... 
    def Convert_Datatype(data):
        #This will convert the datatype of columns from String to integers or Float values
        data['Duration_month'] = float(data['Duration_month']) if 'Duration_month' in data else None
        data['Credit_amount'] = float(data['Credit_amount']) if 'Credit_amount' in data else None
        data['Installment_rate'] = float(data['Installment_rate']) if 'Installment_rate' in data else None
        data['Residential_Duration'] = float(data['Residential_Duration']) if 'Residential_Duration' in data else None
        data['Age'] = float(data['Age']) if 'Age' in data else None
        data['Number_of_credits'] = float(data['Number_of_credits']) if 'Number_of_credits' in data else None
        data['Liable_People'] = float(data['Liable_People']) if 'Liable_People' in data else None
        data['Existing_account'] =  int(data['Existing_account']) if 'Existing_account' in data else None
        data['Credit_history'] =  int(data['Credit_history']) if 'Credit_history' in data else None
        data['Purpose'] =  int(data['Purpose']) if 'Purpose' in data else None
        data['Saving'] =  int(data['Saving']) if 'Saving' in data else None
        data['Employment_duration'] =  int(data['Employment_duration']) if 'Employment_duration' in data else None
        data['Personal_status'] =  int(data['Personal_status']) if 'Personal_status' in data else None
        data['Debtors'] =  int(data['Debtors']) if 'Debtors' in data else None
        data['Property'] =  int(data['Property']) if 'Property' in data else None
        data['Installment_plans'] =  int(data['Installment_plans']) if 'Installment_plans' in data else None
        data['Housing'] =  int(data['Housing']) if 'Housing' in data else None
        data['Job'] =  int(data['Job']) if 'Job' in data else None
        data['Telephone'] =  int(data['Telephone']) if 'Telephone' in data else None
        data['Foreign_worker'] =  int(data['Foreign_worker']) if 'Foreign_worker' in data else None
        return data
    ...
    def run(argv=None, save_main_session=True):
        ...
        with beam.Pipeline(options=PipelineOptions()) as p:
             encoded_data = ( p 
                            | 'Read data' >> beam.io.ReadFromPubSub(topic=TOPIC).with_output_types(bytes) 
                            )
                    data =  ( encoded_data
                            | 'Decode' >> beam.Map(lambda x: x.decode('utf-8') 
                            ) 
              parsed_data = ( data 
                            | 'Parsing Data' >> beam.ParDo(Split())
                            )
           Converted_data = ( parsed_data
                            | 'Convert Datatypes' >> beam.Map(Convert_Datatype)
                            | 'Writing output' >> beam.io.WriteToText(known_args.output))

    if __name__ == '__main__':
        run()
```

7. **Predicting Customer segments**: Now we will implement the machine learning model. If you wish to learn how this machine learning model was created, please visit this [repository](https://github.com/adityasolanki205/German-Credit). We will save this model using JobLib library. To load the sklearn model we will have to follow the steps mentioned below:
    - Download the Model from Google Storage bucket using download_blob method
    
    - Load the model using setup() method in Predict_data() class
    
    - Predict Customer segments from the input data using Predict() method of sklearn
    
    - Add Prediction column in the output

```python
    ... 
    def download_blob(bucket_name=None, source_blob_name=None, project=None, destination_file_name=None):
        storage_client = storage.Client(project)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

    class Predict_Data(beam.DoFn):
        def __init__(self,project=None, bucket_name=None, model_path=None, destination_name=None):
            self._model = None
            self._project = project
            self._bucket_name = bucket_name
            self._model_path = model_path
            self._destination_name = destination_name

        def setup(self):
            """Download sklearn model from GCS"""
            download_blob(bucket_name=self._bucket_name, 
                          source_blob_name=self._model_path,
                          project=self._project, 
                          destination_file_name=self._destination_name)
            self._model = joblib.load(self._destination_name)

        def process(self, element):
            """Predicting using developed model"""
            input_dat = {k: element[k] for k in element.keys()}
            tmp = np.array(list(i for i in input_dat.values()))
            tmp = tmp.reshape(1, -1)
            element['Prediction'] = self._model.predict(tmp).item()
            return [element]
    ...
    def run(argv=None, save_main_session=True):
        ...
        with beam.Pipeline(options=PipelineOptions()) as p:
            encoded_data   = ( p 
                             | 'Read data' >> beam.io.ReadFromPubSub(topic=TOPIC).with_output_types(bytes))
            data           = ( encoded_data
                             | 'Decode' >> beam.Map(lambda x: x.decode('utf-8')) 
            Parsed_data    = ( data 
                             | 'Parsing Data' >> beam.ParDo(Split()))
            Converted_data = ( Parsed_data
                             | 'Convert Datatypes' >> beam.Map(Convert_Datatype))
            Prediction     = ( Converted_data 
                             | 'Predition' >> beam.ParDo(Predict_Data(project=PROJECT_ID, 
                                                         bucket_name='gs://streaming-pipeline-testing', 
                                                         model_path='Selected_Model.pkl',
                                                         destination_name='Selected_model.pkl')))
            Output         = ( Prediction
                             | 'Saving the output' >> beam.io.WriteToText(known_args.output))
    if __name__ == '__main__':
        run()
```

10. **Inserting Data in Bigquery**: Final step in the Pipeline it to insert the data in Bigquery. To do this we will use **beam.io.WriteToBigQuery()** which requires Project id and a Schema of the target table to save the data. 

```python
    import apache_beam as beam
    from apache_beam.options.pipeline_options import PipelineOptions
    import argparse
    
    SCHEMA = 
    '
        Existing_account:INTEGER,
        Duration_month:FLOAT,
        Credit_history:INTEGER,
        Purpose:INTEGER,
        Credit_amount:FLOAT,
        Saving:INTEGER,
        Employment_duration:INTEGER,
        Installment_rate:FLOAT,
        Personal_status:INTEGER,
        Debtors:INTEGER,
        Residential_Duration:FLOAT,
        Property:INTEGER,
        Age:FLOAT,
        Installment_plans:INTEGER,
        Housing:INTEGER,
        Number_of_credits:FLOAT,
        Job:INTEGER,
        Liable_People:FLOAT,
        Telephone:INTEGER,
        Foreign_worker:INTEGER,
        Prediction:INTEGER
    '
    ...
    def run(argv=None, save_main_session=True):
        ...
        parser.add_argument(
          '--project',
          dest='project',
          help='Project used for this Pipeline')
        ...
        PROJECT_ID = known_args.project
        with beam.Pipeline(options=PipelineOptions()) as p:
            encoded_data   = ( p 
                             | 'Read data' >> beam.io.ReadFromPubSub(topic=TOPIC).with_output_types(bytes) 
                             )
            data           = ( encoded_data
                             | 'Decode' >> beam.Map(lambda x: x.decode('utf-8') 
                             ) 
            Parsed_data    = ( data 
                             | 'Parsing Data' >> beam.ParDo(Split()))
            Converted_data = ( Parsed_data
                             | 'Convert Datatypes' >> beam.Map(Convert_Datatype))

            Prediction     = ( Converted_data 
                             | 'Predition' >> beam.ParDo(Predict_Data(project=PROJECT_ID, 
                                                         bucket_name='gs://streaming-pipeline-testing', 
                                                         model_path='Selected_Model.pkl',
                                                         destination_name='Selected_model.pkl')))
            output         = ( Prediction      
                             | 'Writing to bigquery' >> beam.io.WriteToBigQuery(
                               '{0}:GermanCredit.GermanCreditTable'.format(PROJECT_ID),
                               schema=SCHEMA,
                               write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
                             )

    if __name__ == '__main__':
        run()        
```

## Tests
To test the code we need to do the following:

    1. Copy the repository in Cloud SDK using below command:
    git clone https://github.com/adityasolanki205/ML-Streaming-pipeline-using-Dataflow.git
    
    2. Create a Storage Bucket by the name 'streaming-pipeline-testing' in us-east1 with 2 separate subfolders temp and stage 
    
    3. Copy the machine learning model file in the cloud Bucket using the below command
    cd ML-Streaming-pipeline-using-Dataflow
    gsutil cp Selected_model.pkl gs://streaming-pipeline-testing/
    
    3. Create a Dataset in us-east1 by the name GermanCredit
    
    4. Create a table in GermanCredit dataset by the name GermanCreditTable
    
    5. Create Pub Sub Topic by the name german_credit_data
    
    6. Install Apache Beam on the SDK using below command
    sudo pip3 install apache_beam[gcp]
    sudo pip3 install joblib
    sudo pip3 install sklearn
    
    7. Run the command and see the magic happen:
     python3 ml-streaming-pipeline.py \
     --runner DataFlowRunner \
     --project trusty-field-283517 \
     --temp_location gs://streaming-pipeline-testing/temp \
     --staging_location gs://streaming-pipeline-testing/stage \
     --region us-east1 \
     --job_name ml-stream-analysis \
     --save_main_session True \
     --setup_file ./setup.py
     --streaming 
     
    8. Open one more tab in cloud SDK and run below command 
    python3 publish_to_pubsub.py

## Credits
1. Akash Nimare's [README.md](https://gist.github.com/akashnimare/7b065c12d9750578de8e705fb4771d2f#file-readme-md)
2. [Apache Beam](https://beam.apache.org/documentation/programming-guide/#triggers)
3. [Building Data Processing Pipeline With Apache Beam, Dataflow & BigQuery](https://towardsdatascience.com/apache-beam-pipeline-for-cleaning-batch-data-using-cloud-dataflow-and-bigquery-f9272cd89eba)
4. [Let’s Build a Streaming Data Pipeline](https://towardsdatascience.com/lets-build-a-streaming-data-pipeline-e873d671fc57)
5. [Apache Beam + Scikit learn(sklearn)](https://medium.com/@niklas.sven.hansson/apache-beam-scikit-learn-19f8ad10d4d)
