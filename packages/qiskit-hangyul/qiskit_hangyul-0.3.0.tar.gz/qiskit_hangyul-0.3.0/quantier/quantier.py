import json

import qiskit
from concurrent import futures
import dateutil.parser
from typing import Dict, Optional, Tuple, Any, List, Callable, Union

from qiskit.compiler import assemble
from qiskit.providers import  BackendV1
from qiskit.providers.provider import ProviderV1
from qiskit.providers.job import JobV1 as Job
from qiskit.providers.models import BackendConfiguration
 
from qiskit_aer import AerSimulator
from qiskit.providers.options import Options
import mysql.connector as mysql
import os 
from dotenv import load_dotenv
import os

load_dotenv()

class QuantierJob(Job):
    def __init__(self, backend, qobj, **kwargs):
        super().__init__(backend, job_id=self.job_id) # Use actual job_id as per your requirements
        self._backend=backend
        self._job_dict = self.assemble_and_prepare_job(qobj, **kwargs)
        self.json_str = json.dumps(self._job_dict)
        

    def assemble_and_prepare_job(self, qobj, **kwargs):
        job = assemble(qobj).to_dict()
        job['header']['backend_name'] = self._backend.name()
        job['header']['backend_version'] = self._backend.configuration().backend_version
        job['config']['shots'] = kwargs.get('shots', 1024)
        job['config']['memory'] = kwargs.get('memory', False)
        job['config']['parameter_binds'] = kwargs.get('parameter_binds', [])
        return job

    # Following are the mandatory methods to be implemented for a Job.
    def result(self, timeout=None):
        pass  # implement your logic here

    def cancel(self):
        pass  # implement your logic here

    def status(self):
        pass  # implement your logic here

    def backend(self):
        pass  # implement your logic here

    def job_id(self):
        pass  # implement your logic here

    def submit(self):
        pass  # implement your logic here

    def print(self):
        return self.json_str



class QuantierBackend(BackendV1):
    def __init__(self):
        configuration = BackendConfiguration(
            backend_name='quantier_backend',
            backend_version='1.0.0',
            n_qubits=32,
            basis_gates=['x', 'y', 'z', 'h', 'cx', 'id'],
            simulator=True,
            local=True,
            conditional=False,
            open_pulse=False,
            memory=True,
            max_shots=1000000,
            max_experiments=1,
            gates=[],
            coupling_map=None
        )
        self._aer_simulator = AerSimulator()
        super().__init__(configuration=configuration)

    def run(self, qobj, **kwargs):
        print("RUN JOB")
        db = mysql.connect(user=os.environ.get('DB_USERNAME'), 
                             password=os.environ.get('DB_PASSWORD'),
                             host=os.environ.get('DB_HOST'),
                             database=os.environ.get('DB_TYPE'))
        cursor = db.cursor()
        job = QuantierJob(self, qobj, **kwargs)
        
        
        user = os.getcwd().split('/')[-1]
        qobj_json = job.json_str
        cursor.execute('''insert into transaction (qobj_json, email) values (%s, %s)''', (qobj_json, user))
        
        cursor.close()
        db.commit()
        db.close()
        print("SAVED JOB")
        return (job)

        

    @classmethod
    def _default_options(cls):
        return Options()
    





class QuantierProvider(ProviderV1):
    def __init__(self):
        super().__init__()
        self._backend = QuantierBackend()
        self._simulator = AerSimulator()

    def get_backend(self, name=None, **kwargs):
        if name is None or name.lower() == 'quantier_simulator':
            return self._simulator
        elif name.lower() == 'quantier':
            return self._backend
        else:
            raise qiskit.providers.exceptions.QiskitBackendNotFoundError('Backend not found')

    def backends(self, name=None, **kwargs):
        if name is None:
            return [self._simulator, self._backend]
        if name.lower() == 'quantier':
            return [self._backend]
        if name.lower() == 'quantier_simulator':
            return [self._simulator]
        else:
            return []