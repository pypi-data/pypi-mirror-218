# Common Alerting Procotol (CAP) Parser

## What is CAP ?

> *The Common Alerting Protocol (CAP), a digital format for exchanging emergency alerts, allows a consistent alert message to be disseminated simultaneously over multiple communications pathways.*
>
> In *www.fema.gov*

Simply putting, CAP is XML message-formatted based communication focussed one structuring the main aspects of any given emergency in a easy to read / easy to exchange message.
This messages can then be used for communication between devices and for long-term storage in XML files.

It was developed by **Oasis Open**, and full specifications can be found [here](https://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2.html).

*An [example](#example) of a CAP message can be seen bellow*

### Capabilities

- Add rich multimedia such as photographs, maps, streaming video and audio
- Geographically target emergency alerts to a defined warning area. This is limited only by the capacity of the delivery system used.
- Serve the needs of people who are deaf, hard of hearing, blind or low vision.
- Send alerts in multiple languages.

### Example

``` XML
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">
    <identifier>43b080713727</identifier>
    <sender>hsas@dhs.gov</sender>
    <sent>2003-04-02T14:39:01-05:00</sent>
    <status>Actual</status>
    <msgType>Alert</msgType>
    <scope>Private</scope>
    <info>
        <category>Security</category>
        <event>Homeland Security Advisory System Update</event>
        <urgency>Immediate</urgency>
        <severity>Severe</severity>
        <certainty>Likely</certainty>
        <senderName>U.S. Government, Department of Homeland Security</senderName>
        <headline>Homeland Security Sets Code ORANGE</headline>
        <description>The Department of Homeland Security has elevated the Homeland Security Advisory
            System threat level to ORANGE / High in response to intelligence which may indicate a
            heightened threat of terrorism.</description>
        <instruction> A High Condition is declared when there is a high risk of terrorist attacks.
            In addition to the Protective Measures taken in the previous Threat Conditions, Federal
            departments and agencies should consider agency-specific Protective Measures in
            accordance with their existing plans.</instruction>
        <web><http://www.dhs.gov/dhspublic/display?theme=29></web>
        <parameter>
            <valueName>HSAS</valueName>
            <value>ORANGE</value>
        </parameter>
        <resource>
            <resourceDesc>Image file (GIF)</resourceDesc>
            <mimeType>image/gif</mimeType>
            <uri><http://www.dhs.gov/dhspublic/getAdvisoryImage></uri>
        </resource>
        <area>
            <areaDesc>U.S. nationwide and interests worldwide</areaDesc>
        </area>
    </info>
</alert>
```

## How to Use

``` Python
import capparser

alert = capparser.element.Alert(sender="FireTec",
                                status=capparser.enums.Status.Actual,
                                msgType=capparser.enums.MsgType.Alert,
                                scope=capparser.enums.Scope.Private)
alert.setSource("FireTec")
alert.addAddress("Radio Renascenca")

info = capparser.element.Info(category=[capparser.enums.Category.Fire],
                              event="Incendio Florestal em Sever do Vouga",
                              urgency=capparser.enums.Urgency.Immediate,
                              severity=capparser.enums.Severity.Severe,
                              certainty=capparser.enums.Certainty.Observed)
info.setSenderName("FireTec")
info.setInstruction(
    "Foi detetado um possivel incendio florestal na sua area, precaucao e aconselhada.")

param1 = capparser.element.Parameter(parameterName="PS",
                                     parameterValue="PS=Radio Renascenca")
param2 = capparser.element.Parameter(parameterName="PI",
                                     parameterValue="PI=80XX")
param3 = capparser.element.Parameter(parameterName="AF",
                                     parameterValue="AF=95.0")
param4 = capparser.element.Parameter(parameterName="AF",
                                     parameterValue="AF=100.0")
param5 = capparser.element.Parameter(parameterName="AF",
                                     parameterValue="AF=105.0")

info.addParameter(param1)
info.addParameter(param2)
info.addParameter(param3)
info.addParameter(param4)
info.addParameter(param5)

alert.addInfo(info)

capparser.writeAlertToFile(alert, "output.xml")
```
