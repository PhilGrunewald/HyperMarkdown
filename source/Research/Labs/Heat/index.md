% Shift-0
% The MCSCF heat-pump lab


About the Shift-0 heat-pump laboratory
----------------------------------

Shift-0 is a research project, led by the University of Oxford and supported by [MCS Charitable Foundation](https://www.mcscharitablefoundation.org)

Our aims are to

- Learn from heat pump installations to establish best practice
- Use smart-meter data for evidence-led decisions at household and government level
- Provide useful feedback and guidance to existing heat pump owners
- Develop tools to give impartial advice to prospective heat pump adopters


People and partners
-------------------

![](mcscf.png)

Shift-0 is led by [Dr Phil Grunewald, FICE](https://www.oriel.ox.ac.uk/people/dr-phil-grunewald) at the Department of Engineering Science, University of Oxford.

The project is supported by the MCS Charitable Foundation, where
[Richard Hauxwell-Baldwin](https://www.linkedin.com/in/richard-hauxwell-baldwin-a9240858/)
 leads the collaboration.
Research assistants and other contributors will be listed here as the project progresses.

![](oms.svg)

The project was made possible with the kind support of the 
[Oxford Martin School](https://www.oxfordmartin.ox.ac.uk/)
and the Engineering and Physical Sciences Research Council ( [EPSRC](https://www.ukri.org/councils/epsrc) )

![](epsrc.png)


Contact
-------

[](About/People/Phil.html)%box

![](phil.jpg)

For any questions about Shift-0, please contact

[Dr Phil Grünewald](https://www.oriel.ox.ac.uk/people/dr-phil-grunewald)


Department of Engineering Science<br>University of Oxford

Email 
[philipp.grunewald@eng.ox.ac.uk](mailto:philipp.grunewald@eng.ox.ac.uk)

How it works
------------

We access anonymised smart meter data from consenting participants and compare electricity and gas usage before and after heat pump installations. The differences can help us to understand when heat pumps are performing well and under what conditions additional measured can improve their performance.

Find out more about the [research context](about.php)

x!x[](shift0.svg)

x[]x(Register.html)%box



<script>
function validateEmail() {
  const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  const email = document.getElementById('email').value;
  if (!re.test(email)) { 
    document.getElementById('error').innerHTML = 'Please make sure your email is valid'; 
  } else {
    window.location.href = "./sendValidationEmail.php?email=" + email;
    // document.getElementById('error').innerHTML = 'The system is not live yet.'; 
  }
}
</script>
