#    Copyright 2020 SAP SE
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from octavia.db import api as db_api
from octavia.db import repositories
from octavia.f5_extensions import exceptions


def check_member_for_invalid_ip(member_address, load_balancer):
    """When creating a pool member that has the same IP as any VIP in the same network it will lead to error messages
    on the F5 BigIP device, thus making the whole AS3 declaration fail. This function checks the IP address of the
    given member and raises an exception if it finds a conflict. """

    vipRepo = repositories.VipRepository()
    session = db_api.get_session(autocommit=False)

    # get VIPs from network
    conflicts = vipRepo.get(session, network_id=load_balancer.vip.network_id, ip_address=member_address)

    if conflicts:
        raise exceptions.MemberIpConflictingWithVipException(ip=member_address)
