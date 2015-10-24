/*
 * Copyright (c) 2012-2014, TU Delft
 * Copyright (c) 2012-2014, TU Eindhoven
 * Copyright (c) 2012-2014, TU Kaiserslautern
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *
 * 1. Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
 * IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 * TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
 * PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
 * TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * Authors: Karthik Chandrasekar
 *
 */

#include "MemorySpecification.h"
#include "tinyxml2.h"

#include <map>

using namespace std;
using namespace Data;

// Set variable values from XML
void MemorySpecification::processParameters()
{
  setVarFromParam(&id,"memoryId");
  memoryType = getParamValWithDefault("memoryType", string("DDR3"));

  if (hasParameter("memoryType")) {
    memArchSpec.twoVoltageDomains = memoryType.hasTwoVoltageDomains();
    memArchSpec.dll               = memoryType.hasDll();
    memArchSpec.termination       = memoryType.hasTermination();

    memPowerSpec.capacitance = memoryType.getCapacitance();
    memPowerSpec.ioPower     = memoryType.getIoPower();
    memPowerSpec.wrOdtPower  = memoryType.getWrOdtPower();
    memPowerSpec.termRdPower = memoryType.getTermRdPower();
    memPowerSpec.termWrPower = memoryType.getTermWrPower();
  }
}

// Get memspecs from XML
MemorySpecification::MemorySpecification(const std::string& filename) {
  tinyxml2::XMLDocument doc;
  printf("xml filename: %s\n", filename.c_str());
  doc.LoadFile(filename.c_str());
  if (doc.ErrorID()) {
    assert(false && "fail to load xml file" );
  }
  // Build memory specification key-value pairs.
  std::map<std::string, std::string> idinfo;
  std::map<std::string, double> archspec;
  std::map<std::string, double> timingspec;
  std::map<std::string, double> powerspec;

  tinyxml2::XMLElement* root_element = doc.RootElement();

  tinyxml2::XMLElement* id_element = root_element->FirstChildElement("parameter");
  for (tinyxml2::XMLElement* cur = root_element->FirstChildElement("parameter") ;
      cur != NULL ;
      cur = cur->NextSiblingElement("parameter")) {
    const string& spec_id = cur->Attribute("id");
    assert(strcmp(cur->Attribute("type"), "string") == 0);
    idinfo[spec_id] = cur->Attribute("value");
  }

  assert(root_element->FirstChildElement("memarchitecturespec") != NULL);
  for(tinyxml2::XMLElement* cur = root_element->FirstChildElement("memarchitecturespec")->FirstChildElement("parameter") ;
      cur != NULL ;
      cur = cur->NextSiblingElement("parameter")) {
    const string& spec_id = cur->Attribute("id");
    if (strcmp(cur->Attribute("type"), "uint") == 0) {
      archspec[spec_id] = cur->UnsignedAttribute("value");
    } else if (strcmp(cur->Attribute("type"), "double") == 0) {
      archspec[spec_id] = cur->DoubleAttribute("value");
    }
  }

  assert(root_element->FirstChildElement("memtimingspec") != NULL);
  for(tinyxml2::XMLElement* cur = root_element->FirstChildElement("memtimingspec")->FirstChildElement("parameter") ;
      cur != NULL ;
      cur = cur->NextSiblingElement("parameter")) {
    const string& spec_id = cur->Attribute("id");
    if (strcmp(cur->Attribute("type"), "uint") == 0) {
      timingspec[spec_id] = cur->UnsignedAttribute("value");
    } else if (strcmp(cur->Attribute("type"), "double") == 0) {
      timingspec[spec_id] = cur->DoubleAttribute("value");
    }
  }

  assert(root_element->FirstChildElement("mempowerspec") != NULL);
  for(tinyxml2::XMLElement* cur = root_element->FirstChildElement("mempowerspec")->FirstChildElement("parameter") ;
      cur != NULL ;
      cur = cur->NextSiblingElement("parameter")) {
    const string& spec_id = cur->Attribute("id");
    if (strcmp(cur->Attribute("type"), "uint") == 0) {
      powerspec[spec_id] = cur->UnsignedAttribute("value");
    } else if (strcmp(cur->Attribute("type"), "double") == 0) {
      powerspec[spec_id] = cur->DoubleAttribute("value");
    }
  }

  std::string id = idinfo["memoryId"];
  memoryType = MemoryType(idinfo["memoryType"]);

  if (hasParameter("memoryType")) {
    memArchSpec.twoVoltageDomains = memoryType.hasTwoVoltageDomains();
    memArchSpec.dll               = memoryType.hasDll();
    memArchSpec.termination       = memoryType.hasTermination();

    memPowerSpec.capacitance = memoryType.getCapacitance();
    memPowerSpec.ioPower     = memoryType.getIoPower();
    memPowerSpec.wrOdtPower  = memoryType.getWrOdtPower();
    memPowerSpec.termRdPower = memoryType.getTermRdPower();
    memPowerSpec.termWrPower = memoryType.getTermWrPower();
  }

  // memArchSpec
  if (archspec.count("burstLength") == 1) {
    memArchSpec.burstLength = archspec["burstLength"];
  } if (archspec.count("nbrOfBanks") == 1) {
    memArchSpec.nbrOfBanks = archspec["nbrOfBanks"];
  } if (archspec.count("nbrOfRanks") == 1) {
    memArchSpec.nbrOfRanks = archspec["nbrOfRanks"];
  } if (archspec.count("dataRate") == 1) {
    memArchSpec.dataRate = archspec["dataRate"];
  } if (archspec.count("nbrOfColumns") == 1) {
    memArchSpec.nbrOfColumns = archspec["nbrOfColumns"];
  } if (archspec.count("nbrOfRows") == 1) {
    memArchSpec.nbrOfRows = archspec["nbrOfRows"];
  } if (archspec.count("width") == 1) {
    memArchSpec.width = archspec["width"];
  } if (archspec.count("nbrOfBankGroups") == 1) {
    memArchSpec.nbrOfBankGroups = archspec["nbrOfBankGroups"];
  }

  // memTimingSpec
  if (timingspec.count("clkMhz") == 1) {
    memTimingSpec.clkMhz =timingspec["clkMhz"];
    memTimingSpec.clkPeriod = 1000.0 / timingspec["clkMhz"];
  } if (timingspec.count("RC") == 1) {
    memTimingSpec.RC = timingspec["RC"];
  } if (timingspec.count("RCD") == 1) {
    memTimingSpec.RCD = timingspec["RCD"];
  } if (timingspec.count("CCD") == 1) {
    memTimingSpec.CCD = timingspec["CCD"];
  } if (timingspec.count("CCD_S") == 1) {
    memTimingSpec.CCD_S = timingspec["CCD_S"];
  } if (timingspec.count("CCD_L") == 1) {
    memTimingSpec.CCD_L = timingspec["CCD_L"];
  } if (timingspec.count("RRD") == 1) {
    memTimingSpec.RRD = timingspec["RRD"];
  } if (timingspec.count("RRD_S") == 1) {
    memTimingSpec.RRD_S = timingspec["RRD_S"];
  } if (timingspec.count("RRD_L") == 1) {
    memTimingSpec.RRD_L = timingspec["RRD_L"];
  } if (timingspec.count("FAW") == 1) {
    memTimingSpec.FAW = timingspec["FAW"];
  } if (timingspec.count("TAW") == 1) {
    memTimingSpec.TAW = timingspec["TAW"];
  } if (timingspec.count("WTR") == 1) {
    memTimingSpec.WTR = timingspec["WTR"];
  } if (timingspec.count("WTR_S") == 1) {
    memTimingSpec.WTR_S = timingspec["WTR_S"];
  } if (timingspec.count("WTR_L") == 1) {
    memTimingSpec.WTR_L = timingspec["WTR_L"];
  } if (timingspec.count("REFI") == 1) {
    memTimingSpec.REFI = timingspec["REFI"];
  } if (timingspec.count("RL") == 1) {
    memTimingSpec.RL = timingspec["RL"];
  } if (timingspec.count("RP") == 1) {
    memTimingSpec.RP = timingspec["RP"];
  } if (timingspec.count("RFC") == 1) {
    memTimingSpec.RFC = timingspec["RFC"];
  } if (timingspec.count("RAS") == 1) {
    memTimingSpec.RAS = timingspec["RAS"];
  } if (timingspec.count("WL") == 1) {
    memTimingSpec.WL = timingspec["WL"];
  } if (timingspec.count("WL") == 1) {
    memTimingSpec.AL = timingspec["AL"];
  } if (timingspec.count("DQSCK") == 1) {
    memTimingSpec.DQSCK = timingspec["DQSCK"];
  } if (timingspec.count("RTP") == 1) {
    memTimingSpec.RTP = timingspec["RTP"];
  } if (timingspec.count("WR") == 1) {
    memTimingSpec.WR = timingspec["WR"];
  } if (timingspec.count("XP") == 1) {
    memTimingSpec.XP = timingspec["XP"];
  } if (timingspec.count("XPDLL") == 1) {
    memTimingSpec.XPDLL = timingspec["XPDLL"];
  } if (timingspec.count("XS") == 1) {
    memTimingSpec.XS = timingspec["XS"];
  } if (timingspec.count("XSDLL") == 1) {
    memTimingSpec.XSDLL = timingspec["XSDLL"];
  } if (timingspec.count("CKE") == 1) {
    memTimingSpec.CKE = timingspec["CKE"];
  } if (timingspec.count("CKESR") == 1) {
    memTimingSpec.CKESR = timingspec["CKESR"];
  }

  // memPowerSpec
  if (powerspec.count("idd0") == 1) {
    memPowerSpec.idd0 = powerspec["idd0"];
  } if (powerspec.count("idd02") == 1) {
    memPowerSpec.idd02 = powerspec["idd02"];
  } if (powerspec.count("idd2p0") == 1) {
    memPowerSpec.idd2p0 = powerspec["idd2p0"];
  } if (powerspec.count("idd2p02") == 1) {
    memPowerSpec.idd2p02 = powerspec["idd2p02"];
  } if (powerspec.count("idd2p1") == 1) {
    memPowerSpec.idd2p1 = powerspec["idd2p1"];
  } if (powerspec.count("idd2p12") == 1) {
    memPowerSpec.idd2p12 = powerspec["idd2p12"];
  } if (powerspec.count("idd2n") == 1) {
    memPowerSpec.idd2n = powerspec["idd2n"];
  } if (powerspec.count("idd2n2") == 1) {
    memPowerSpec.idd2n2 = powerspec["idd2n2"];
  } if (powerspec.count("idd3p0") == 1) {
    memPowerSpec.idd3p0 = powerspec["idd3p0"];
  } if (powerspec.count("idd3p02") == 1) {
    memPowerSpec.idd3p02 = powerspec["idd3p02"];
  } if (powerspec.count("idd3p1") == 1) {
    memPowerSpec.idd3p1 = powerspec["idd3p1"];
  } if (powerspec.count("idd3p12") == 1) {
    memPowerSpec.idd3p12 = powerspec["idd3p12"];
  } if (powerspec.count("idd3n") == 1) {
    memPowerSpec.idd3n = powerspec["idd3n"];
  } if (powerspec.count("idd3n2") == 1) {
    memPowerSpec.idd3n2 = powerspec["idd3n2"];
  } if (powerspec.count("idd4r") == 1) {
    memPowerSpec.idd4r = powerspec["idd4r"];
  } if (powerspec.count("idd4r2") == 1) {
    memPowerSpec.idd4r2 = powerspec["idd4r2"];
  } if (powerspec.count("idd4w") == 1) {
    memPowerSpec.idd4w = powerspec["idd4w"];
  } if (powerspec.count("idd4w2") == 1) {
    memPowerSpec.idd4w2 = powerspec["idd4w2"];
  } if (powerspec.count("idd5") == 1) {
    memPowerSpec.idd5 = powerspec["idd5"];
  } if (powerspec.count("idd52") == 1) {
    memPowerSpec.idd52 = powerspec["idd52"];
  } if (powerspec.count("idd6") == 1) {
    memPowerSpec.idd6 = powerspec["idd6"];
  } if (powerspec.count("idd62") == 1) {
    memPowerSpec.idd62 = powerspec["idd62"];
  } if (powerspec.count("vdd") == 1) {
    memPowerSpec.vdd = powerspec["vdd"];
  } if (powerspec.count("vdd2") == 1) {
    memPowerSpec.vdd2 = powerspec["vdd2"];
  }
}
