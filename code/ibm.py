from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer

def create_and_measure(d):

	q = QuantumRegister(3)
	c = ClassicalRegister(3)
	ghz = QuantumCircuit(q, c)

	# ghz.x(q)
	ghz.h(q[0])
	ghz.h(q[1])
	ghz.x(q[2])

	ghz.cx(q[1],q[2])
	ghz.cx(q[0],q[2])

	ghz.h(q[0])
	ghz.h(q[1])
	ghz.h(q[2])

	ghz.barrier()


	# ---------- performing measurement
	if d[0] == 'x':
		if d[1]  == 'x':
			ghz.h(q[0])
			ghz.h(q[1])
			ghz.h(q[2])
			# XXX
		else:
			ghz.h(q[0])
			ghz.sdg(q[1])
			ghz.sdg(q[2])
			ghz.h(q[1])
			ghz.h(q[2])
			# XYY
	else:


		if d[1]  == 'x':
			ghz.sdg(q[0])
			ghz.h(q[1])
			ghz.sdg(q[2])

			ghz.h(q[0])
			ghz.h(q[2])
			# YXY
		else:
			ghz.sdg(q[0])
			ghz.sdg(q[1])
			ghz.h(q[2])
			ghz.h(q[0])
			ghz.h(q[1])
			# YYX


	ghz.measure(q[0], c[0])
	ghz.measure(q[1], c[1])
	ghz.measure(q[2], c[2])


	job = execute(ghz, backend = Aer.get_backend('qasm_simulator'), shots=1)
	result = job.result()

	return result.get_counts(ghz)

	# # # Print the result
	# print(result.get_counts(ghz))
	# print(result.get_counts(ghz))