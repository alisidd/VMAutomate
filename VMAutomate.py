import requests, sys, inspect

from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession

from cobra.mit.request import ConfigRequest, DnQuery

from cobra.model.fv import Ap, AEPg, RsBd, Ctx, BD, RsCtx, RsDomAtt, RsCustQosPol
from cobra.model.vz import Filter, Entry, BrCP, Subj, RsSubjFiltAtt

from cobra.model.vmm import ProvP, DomP, UsrAccP, CtrlrP, RsAcc

requests.packages.urllib3.disable_warnings()

# Enter login details for apic
username = "admin"
password = "1vtG@lw@y"

# Enter apic address
protocol = "https"
host = "10.10.10.33"

apic = "{0}://{1}".format(protocol, host)

session = LoginSession(apic, username, password)
moDir = MoDirectory(session)
moDir.login()

if __name__ == "__main__":

    # Enter tenant, application profile where VMM exists
    tenant = "infra"
    ap = "access"

    # Making a new epg and calling it "vmepg"
    application_profile = moDir.lookupByDn("uni/tn-{0}/ap-{1}".format(tenant, ap))

    new_epg = AEPg(application_profile, "vmepg")

    # Committing the changes
    config_request = ConfigRequest()
    config_request.addMo(new_epg)

    moDir.commit(config_request)

    # Enter epg to use as template for vmepg
    epg_template= "default"

    dnQuery = DnQuery('uni/tn-{0}/ap-{1}/epg-{2}'.format(tenant, ap, epg_template))
    dnQuery.subtree = 'children'
    epgMO = moDir.query(dnQuery)

    # Traversing every property within epg_template and copying it to vmepg
    for epg in epgMO:
        for epgChild in epg.children:
            for name, obj in inspect.getmembers(sys.modules[__name__]):
                if inspect.isclass(obj):
                    copy_of_property = str(epgChild.rn)
                    if (copy_of_property.lower().startswith(obj.__name__.lower())):
                        exec("object_made = " + obj.__name__ + "(epg, \"" + copy_of_property + "\")")

                        config_request.addMo(object_made)
                        moDir.commit(config_request)
