# Setup a virtual env to install the package (recommended):
python -m venv venv
# On Unix OS:
source ./venv/bin/activate 
# On Windows:
venv\Scripts\activate
# Install dependencies:
pip install -r requirements .
# Install the actual package:
pip install --upgrade . 
# Uninstalling:
pip uninstall srflp_solver
# Input example:
<pre>
{
    "n": 6,
    "F": [1, 2, 3, 4, 5, 6],
    "L": [20, 10, 16, 20, 10, 10],
    "C": [
        [-1, 12, 3, 6, 0, 20],
        [12, -1, 3, 6, 0, 20],
        [3, 5, -1, 6, 0, 20],
        [6, 5, 3, -1, 0, 20],
        [0, 5, 3, 6, -1, 20],
        [20, 0, 3, 6, 0, -1]
    ]
}
</pre>