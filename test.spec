// ——————————
// Library
// ——————————

fn fold<E, I>(list: List<E>, f: (I, E)->I, init: I) -> I {
    if len(list) == 0 {
        init
    } else {
        fold::<E, I>(list[1..], f, f(init, list[0]))
    }
}

fn map<S, T>(list: List<S>, f: (S)->T) -> List<T> {
    fold::<S, List<T>>(
        list, 
        |mapped, elem| {
            mapped ++ [f(elem)]
        },
        [],
    )
}

fn filter<E>(list: List<E>, f: (E)->Bool) -> List<E> {
    fold::<E, List<E>>(
        list, 
        |filtered, elem| {
            filtered ++ if f(elem) { [elem] } else { [] }
        },
        [],
    )
}

fn max<E>(list: List<E>, f: (E)->Int) -> Int {
    fold::<E, Int>(
        list, 
        |res, elem| {
            let new = f(elem);
            if new >s res { new } else { res }
        },
        0,
    )
}

fn any<E>(list: List<E>, f: (E)->Bool) -> Bool {
    fold::<E, Bool>(
        list,
        |res, elem| { res || f(elem) },
        false,
    )
}

fn all<E>(list: List<E>, f: (E)->Bool) -> Bool {
    fold::<E, Bool>(
        list,
        |res, elem| { res && f(elem) },
        true,
    )
}

fn rev<E>(list: List<E>) -> List<E> {
    fold::<E, List<E>>(
        list,
        |res, elem| { [elem] ++ res },
        [],
    )
}

fn fold2<A, B, I>(
    l0: List<A>,
    l1: List<B>,
    f: (I, A, B) -> I,
    init: I,
) -> I {
    let len0 = len(l0);
    let len1 = len(l1);
    if len0 == 0 || len1 == 0 {
        init
    } else {
        fold2::<A, B, I>(l0[1..], l1[1..], f, f(init, l0[0], l1[0]))
    }
}

fn list_eq<E>(l0: List<E>, l1: List<E>) -> Bool {
    let len0 = len(l0);
    let len1 = len(l1);
    len0 == len1
    && fold2::<E, E, Bool>(
        l0,
        l1,
        |eq, elem0, elem1| { eq && elem0 == elem1 },
        true,
    )
}

fn list_eq_by<E>(l0: List<E>, l1: List<E>, cmp: (E, E)->Bool) -> Bool {
    let len0 = len(l0);
    let len1 = len(l1);
    len0 == len1
    && fold2::<E, E, Bool>(
        l0,
        l1,
        |eq, elem0, elem1| { eq && cmp(elem0, elem1) },
        true,
    )
}

struct ListCmp {
    cnt: Int,
    diff: Bool,
}
fn list_cmp<E>(l0: List<E>, l1: List<E>) -> Int {
    fold2::<E, E, ListCmp>(
        l0,
        l1,
        |cmp, elem0, elem1| {
            if !cmp.diff && elem0 == elem1 {
                ListCmp {
                    cnt: cmp.cnt + 1,
                    diff: false,
                }
            } else {
                ListCmp {
                    cnt: cmp.cnt,
                    diff: true,
                }
            }
        },
        ListCmp {
            cnt: 0,
            diff: false,
        },
    ).cnt
}


// ——————————
// Type Definitions
// ——————————

struct Opaque { }

struct String {
    data: &Int<8>,
    len: Int<64>,
}

struct ByteSlice {
    data: &Int<8>,
    len: Int<64>,
    cap: Int<64>,
}

use %IPST.4 as struct StringSlice {
    data: &String,
    len: Int<64>,
    cap: Int<64>,
}

use %IPST.0 as struct RRSlice {
    data: &ResourceRecord,
    len: Int<64>,
    cap: Int<64>,
}

use %IPST.3 as struct QuestionSlice {
    data: &Question,
    len: Int<64>,
    cap: Int<64>,
}

use %IPST.8 as struct PtrZoneSlice {
    data: & &Zone,
    len: Int<64>,
    cap: Int<64>,
}

struct Map {
    _0: Int<64>,
    _1: Int<8>,
    _2: Int<8>,
    _3: Int<16>,
    _4: Int<32>,
    _5: &Int<8>,
    _6: &Int<8>,
    _7: Int<64>,
    _8: &Int<8>,
}

use %Request.0 as struct Request {
    msg: &Msg,
    w: ResponseWriter,
    zone: String,
    size: Int<16>,
    do: Int<8>,

    family: Int<8>,
    name: String,
    ip: String,
    port: String,
    local_port: String,
    local_ip: String,
}

use %Zone.0 as struct Zone {
    origin: String,
    orig_len: Int<64>,
    file: String,
    tree: &Tree,
    apex: Apex,
    expired: Int<8>,

    rwmutex: RWMutex,
    start_up_once: Once,
    transfer_from: StringSlice,

    reload_interval: Int<64>,
    reload_shutdown: &Opaque,
    upstream: &Upstream,
}

use %Tree.0 as struct Tree {
    root: &Node,
    count: Int<64>,
}

use %Node.0 as struct Node {
    elem: &Elem,
    left: &Node,
    right: &Node,
    color: Int<8>,
}

use %Elem.0 as struct Elem {
    m: &Map,
    name: String,
}

use %RR.0 as struct ResourceRecord {
    itab: &RRItab,
    data: &Int<8>,
}

use %RR_Header.0 as struct RRHeader {
    name: String,
    rrtype: Int<16>,
    class: Int<16>,
    ttl: Int<32>,
    rdlength: Int<16>,
}

struct GoInterface {
    itab: &Int<8>,
    data: &Int<8>,
}

// Interface table for RRs
struct RRItab {
    type: &GoType,
    header: &(&Int<8>, &Int<8>) -> &RRHeader,
    copy: &(&Int<8>, &Int<8>) -> &GoInterface,
}

use %Msg.0 as struct Msg {
    header: MsgHdr,
    compress: Int<8>,
    question: QuestionSlice,
    answer: RRSlice,
    ns: RRSlice,
    extr: RRSlice,
}

use %Question.0 as struct Question {
    name: String,
    qtype: Int<16>,
    qclass: Int<16>,
}

use %MsgHdr.0 as struct MsgHdr {
    id: Int<16>,
    response: Int<8>,
    opcode: Int<64>,
    authoritative: Int<8>,
    truncated: Int<8>,
    recursion_desired: Int<8>,
    recursion_available: Int<8>,
    zero: Int<8>,
    authenticated_data: Int<8>,
    checking_disabled: Int<8>,
    rcode: Int<64>,
}

use %Apex.0 as struct Apex {
    soa: &Soa,
    ns: RRSlice,
    sigsoa: RRSlice,
    signs: RRSlice,
}

use %SOA.0 as struct Soa
use %error.0 as struct GoError
use %_type.0 as struct GoType
use %ResponseWriter.0 as struct ResponseWriter
use %RWMutex.0 as struct RWMutex
use %Once.0 as struct Once
use %__go_descriptor.2 as struct GoDescriptor2
use %uncommonType.0 as struct GoUncommonType

// ——————————
// String SPECs
// ——————————

fn string_spec(
    p: &Int<8>, 
    n: Int<64>,
) -> Bool {
    specialize(n) &&
    if n == 0w64 {
        true
    } else {
        __string_spec(p, n)
    }
}

fn __string_spec(p: &Int<8>, n: Int<64>) -> Bool {
    let ch = *p;
    specialize(ch) &&
    if n <= 1w64 { 
        true 
    } else { 
        __string_spec(p[1], n - 1w64) 
    }
}

fn string_noescape(
    p: &Int<8>, 
    n: Int<64>,
) -> Bool {
    specialize(n) &&
    if n == 0w64 {
        true
    } else {
        __string_noescape(p, n)
    }
}

fn __string_noescape(p: &Int<8>, n: Int<64>) -> Bool {
    let ch = *p;
    ch != 92w8 &&
    if n <= 1w64 { 
        true 
    } else { 
        __string_noescape(p[1], n - 1w64) 
    }
}



// ——————————
// CDNS SPECs
// ——————————

// { i8*, i64 } @go.coredns.Request.Name(i8* nest nocapture readnone %nest.4, %Request.0* %r)
fn go_coredns_request_name_oracle(
    _: &Int<8>,
    r: &Request,
) -> String {
    let msg = *r.msg;
    let question = *msg.question.data;
    *question.name
}

// i64 @go.coredns.Request.Size(i8* nest nocapture readnone %nest.7, %Request.0* %r)
fn go_coredns_request_size_oracle(
    _: &Int<8>,
    r: &Request,
) -> Int<64> {
    65535w64
}

// i64 go.coredns.CompareDomainName(i8* nest nocapture readnone %nest.35, i8* readonly %s1.chunk0, i64 %s1.chunk1, i8* readonly %s2.chunk0, i64 %s2.chunk1)
fn go_coredns_compare_domain_name_oracle(
    _: &Int<8>,
    data1: &Int<8>, len1: Int<64>,
    data2: &Int<8>, len2: Int<64>,
) -> Int<64> {
    // Specialize the lengths
    let _ = specialize(len1) && specialize(len2);

    // If either is the root label or empty, return 0
    if len1 == 0w64
        || len2 == 0w64
        || (len1 == 1w64 && *data1 == 46w8) 
        || (len2 == 1w64 && *data2 == 46w8) {
        0w64 
    } else {
        // CompareDomainName requires both strings to be syntactically valid;
        // part of that means they must end with a dot(.).
        // If that is not the case, this function as written returns 0.
        if *data1[len1 - 1w64] != 46w8 || *data2[len2 - 1w64] != 46w8 {
            0w64
        } else {
            // Compare recursively, backwards
            __compare_domain_name(data1, len1-2w64, data2, len2-2w64)
        }
    }
}

// ..end of a label?
fn __compare_domain_name_eol(data: &Int<8>, i: Int<64>) -> Bool {
    i <s 0w64 || *data[i] == 46w8
}

fn __compare_domain_name(data1: &Int<8>, i1: Int<64>, data2: &Int<8>, i2: Int<64>) -> Int<64> {

    // Increment if both currently at the end of a label
    let inc = if __compare_domain_name_eol(data1, i1) && __compare_domain_name_eol(data2, i2) {
        1w64
    } else {
        0w64
    };

    // Stop if either overshots, or mismatches
    let stop = i1 <s 0w64
        || i2 <s 0w64
        || *data1[i1] != *data2[i2];

    if stop {
        inc
    } else {
        inc + __compare_domain_name(data1, i1 - 1w64, data2, i2 - 1w64)
    }
}

struct ZoneLookupSret {
    _0: RRSlice,
    _1: RRSlice,
    _2: RRSlice,
    _3: Int<64>,
}

// void @go.coredns.Zone.Lookup({ %IPST.0, %IPST.0, %IPST.0, i64 }* sret %sret.formal.1, i8* nest nocapture readnone %nest.2, %Zone.0* %z, i8* %ctx.chunk0, i8* %ctx.chunk1, %Request.0* byval %state, i8* %qname.chunk0, i64 %qname.chunk1)
fn go_coredns_zone_lookup_precond(
    sret: &ZoneLookupSret,
    _: &Int<8>,
    zone: &Zone,
    loop_count: &Int<8>,
    file: &Int<8>,
    state: &Request, 
    qname0: &Int<8>,
    qname1: Int<64>,
) -> Bool {
    specialize(loop_count)
    && specialize(qname1) // TODO: this is buggy...why?
}

// { i8*, i8 } go.coredns.Tree.Prev(i8* nest nocapture readnone %nest.10, %Tree.0* readonly %t, i8* %qname.chunk0, i64 %qname.chunk1)
fn go_coredns_tree_prev_precond(_: &Int<8>, tree: &Tree, data: &Int<8>, len: Int<64>) -> Bool {
    specialize(len)
}

// { i8*, i8 } go.coredns.Tree.Next(i8* nest nocapture readnone %nest.11, %Tree.0* readonly %t, i8* %qname.chunk0, i64 %qname.chunk1)
fn go_coredns_tree_next_precond(_: &Int<8>, tree: &Tree, data: &Int<8>, len: Int<64>) -> Bool {
    specialize(len)
}

// { i8*, i8 } go.coredns.Node.search(i8* nest nocapture readnone %nest.9, %Node.0* %n, i8* %qname.chunk0, i64 %qname.chunk1)
fn go_coredns_node_search_precond(_: &Int<8>, node: &Node, data: &Int<8>, len: Int<64>) -> Bool {
    specialize(node)
    && specialize(len)
}

struct StringAndBool {
    string: String,
    bool: Int<8>,
}

// void go.coredns.Zone.nameFromRight({ { i8*, i64 }, i8 }* nocapture sret %sret.formal.3, i8* nest nocapture readnone %nest.12, %Zone.0* readonly %z, i8* %qname.chunk0, i64 %qname.chunk1, i64 %i)
fn go_coredns_zone_name_from_right_precond(
    sret: &StringAndBool,
    _: &Int<8>,
    zone: &Zone,
    data: &Int<8>, 
    len: Int<64>,
    i: Int<64>,
) -> Bool {
    specialize(len)
    && specialize(i)
}

// { i8*, i64 } go.coredns.sprintName(i8* nest nocapture readnone %nest.60, i8* %s.chunk0, i64 %s.chunk1)
fn go_coredns_sprint_name_precond(_: &Int<8>, data: &Int<8>, len: Int<64>) -> Bool {
    specialize(len)
}


// { i8*, i64 } go.coredns.Join(i8* nest nocapture readnone %nest.42, %IPST.4* nocapture readonly byval %labels)
fn go_coredns_join_precond(_: &Int<8>, labels: &StringSlice) -> Bool {
    let len = *labels.len;
    specialize(len)
    && __go_coredns_join_precond(*labels.data, 0w64, len)
}

fn __go_coredns_join_precond(p: &String, i: Int<64>, n: Int<64>) -> Bool {
    if i >=s n {
        true
    } else {
        let str = *p[i];
        specialize(str.len)
        && __go_coredns_join_precond(p, i + 1w64, n)
    }
}

// i8 go.coredns.IsSubDomain(i8* nest nocapture readnone %nest.27, i8* readonly %parent.chunk0, i64 %parent.chunk1, i8* readonly %child.chunk0, i64 %child.chunk1)
fn go_coredns_is_subdomain_precond(_: &Int<8>, data1: &Int<8>, len1: Int<64>, data2: &Int<8>, len2: Int<64>) -> Bool {
    specialize(len1)
    && specialize(len2)
}

// i64 go.coredns.CountLabel(i8* nest nocapture readnone %nest.38, i8* readonly %s.chunk0, i64 %s.chunk1)
fn go_coredns_count_label_precond(_: &Int<8>, data: &Int<8>, len: Int<64>) -> Bool {
    specialize(len)
}

// i64 go.coredns.Less(i8* %nest.48, %Elem.0* %a, i8* %name.chunk0, i64 %name.chunk1)
fn go_coredns_less_precond(_: &Int<8>, elem: &Elem, data: &Int<8>, len: Int<64>) -> Bool {
    let elen = *elem.name.len;
    specialize(elen)
}

// { i64, i8 } go.coredns.PrevLabel(i8* %nest.31, i8* %s.chunk0, i64 %s.chunk1, i64 %n)
fn go_coredns_prev_label_precond(_: &Int<8>, data: &Int<8>, len: Int<64>, n: Int<64>) -> Bool {
    specialize(n)
    && string_noescape(data, len)
}

// { i64, i8 } go.coredns.NextLabel(i8* nest nocapture readnone %nest.32, i8* nocapture readonly %s.chunk0, i64 %s.chunk1, i64 %offset)
fn go_coredns_next_label_precond(_: &Int<8>, data: &Int<8>, len: Int<64>, offset: Int<64>) -> Bool {
    specialize(offset)
    && string_noescape(data, len)
}

// i8 go.coredns.IsFqdn(i8* nest nocapture readnone %nest.57, i8* %s.chunk0, i64 %s.chunk1)
fn go_coredns_is_fqdn_precond(_: &Int<8>, data: &Int<8>, len: Int<64>) -> Bool {
    string_noescape(data, len)
}

// go.coredns.doDDD( {i8*, i64, i64}* %b )
fn go_coredns_doddd_precond(b: &ByteSlice) -> Bool {
    let data = *b.data;
    let len = *b.len;
    string_noescape(data, len)
}


// ——————————
// Top Level
// ——————————

struct Sret {
   rcode: Int<64>,
   error: GoError,
}

use %File.0 as struct File {
    zones: Zones,
}

use %Zones.0 as struct Zones {
    z: PtrZoneSlice,
}

use @go.coredns.File.ServeDNS as fn coredns_rrlookup(
    &Sret,
    &Int<8>,
    &File,
    &Int<8>,
    &Int<8>,
    &Int<8>,
    &Int<8>,
    &Msg,
);

struct Verdict {
    ok: Bool,
    coredns: DnsResponse,
    model: DnsResponse,
}

fn verify_coredns(
    sret: &Sret,
    file: &File,
    request: &Request,
) -> Verdict {

    let dns_zone = into_dns_zone(file);
    let dns_query = into_dns_query(request);

    let empty = DnsResponse {
        rcode: DnsRCode.NOERROR,
        flag_aa: true,
        answer: [],
        authority: [],
        additional: [],
    };

    if !valid_query(dns_query, dns_zone.zone_name) {
        // Non-valid queries are omitted
        Verdict {
            ok: true,
            coredns: empty,
            model: empty,
        }
    } else {
        
        // Get model's response
        let dns_resp = rrlookup(dns_zone, dns_query);

        // Get coredns's response
        let p = request.w as &Int<8>;
        let w0 = *(p as & &Int<8>);
        let w1 = *(p[8] as & &Int<8>);
        let r = *request.msg;

        let _ = coredns_rrlookup(
            sret,
            havoc,
            file,
            null,               // ctx0: loop_count
            file as &Int<8>,    // ctx1: file
            w0,
            w1,
            r,
        );
        let resp = into_dns_response(r);
        
        // Response equality means verification
        let ok = resp.rcode == dns_resp.rcode
        && resp.flag_aa == dns_resp.flag_aa
        && list_eq_by::<DnsRecord>(resp.answer, dns_resp.answer, compare_rr)
        && list_eq_by::<DnsRecord>(resp.authority, dns_resp.authority, compare_rr)
        && list_eq_by::<DnsRecord>(resp.additional, dns_resp.additional, compare_rr);

        if ok {
            Verdict {
                ok: true,
                coredns: resp,
                model: dns_resp,
            }
        } else {
            Verdict {
                ok: false,
                coredns: resp,
                model: dns_resp,
            }
        }
    }
}

// Compare two DnsRecords.
fn compare_rr(rr1: DnsRecord, rr2: DnsRecord) -> Bool {
    rr1.rtype == rr2.rtype
    && list_eq::<Int<8>>(rr1.rname, rr2.rname)
    && list_eq::<Int<8>>(rr1.rdata, rr2.rdata)
}

fn valid_query(
    query: DnsQuery,
    origin: List<Int<8>>,
) -> Bool {
    let qname = query.qname;
    query.qtype != DnsRRType.XFR
    && query.qtype != DnsRRType.DS
    && is_parent(origin, qname) 
    && fold2::<Int<8>, Int<8>, Bool>(
        qname,
        [46w8] ++ qname,
        |ok, e1, e2| { ok && !(e1 == 46w8 && e2 == 46w8) },
        true
    )
}

// Make a DnsZone from a coredns `File`
fn into_dns_zone(file: &File) -> DnsZone {
    let zone = **file.zones.z.data;
    let origin0 = *zone.origin.data;
    let origin1 = *zone.origin.len;
    let zone_name = into_dns_name(origin0, origin1); 
    let soa = *zone.apex.soa;
    let ns = *zone.apex.ns;
    let apex_rrs = [into_dns_record(soa as &Int<8>)]
        ++ dns_records_from_slice(ns.data, ns.len);

    let root = *(*zone.tree).root;
    DnsZone {
        zone_name: zone_name,
        rrs: apex_rrs ++ into_dns_records(root),
    }
}

// Make DnsQuery's from a coredns `Request`
fn into_dns_query(request: &Request) -> DnsQuery {
    let msg = *request.msg;
    let _ = specialize(*msg.header.opcode); // hdr.opcode
    let question = msg.question;
    let _ = specialize(*question.len);
    let qdata = *question.data;
    let qname = *qdata.name;
    let qname0 = qname.data;
    let qname1 = qname.len;
    let qname = into_dns_name(qname0, qname1);
    let qtype = *qdata.qtype;
    
    DnsQuery {
        qname: qname,
        qtype: into_dns_rrtype(qtype),
    }
}

// Make a DnsResponse from a coredns `Msg`
fn into_dns_response(msg: &Msg) -> DnsResponse {
    let rcode = *msg.header.rcode;
    let flag_aa = if *msg.header.authoritative != 0w8 { true } else { false };
    let answer = dns_records_from_slice(
        *msg.answer.data,
        *msg.answer.len,
    );
    let authority = dns_records_from_slice(
        *msg.ns.data,
        *msg.ns.len,
    );
    let additional = dns_records_from_slice(
        *msg.extr.data,
        *msg.extr.len,
    );

    DnsResponse {
        rcode: into_dns_rcode(rcode),
        flag_aa: flag_aa,
        answer: ordered(answer),
        authority: ordered(authority),
        additional: ordered(additional),
    }
}

fn into_dns_rcode(rcode: Int<64>) -> DnsRCode {
    let _ = specialize(rcode);
    if rcode == 0w64 {
        DnsRCode.NOERROR
    } else {
        if rcode == 3w64 {
            DnsRCode.NXDOMAIN
        } else {
            DnsRCode.OTHER
        }
    }
}

// Map a coredns `Node` into a list of DnsRecords (in the entire sub-tree).
fn into_dns_records(node: &Node) -> List<DnsRecord> {
    if node == null {
        []
    } else {
        let rrslices: List<&Int<8>> = values(*(*node.elem).m); // HACK
        into_dns_records(*node.left)
        ++
        fold::<&Int<8>, List<DnsRecord>>(
            rrslices,
            |acc, rrslice| { 
                let rrslice = rrslice as &RRSlice;
                let data = *rrslice.data;
                let len = *rrslice.len;
                acc ++ dns_records_from_slice(data, len)
            },
            [],
        ) 
        ++
        into_dns_records(*node.right)
    }
}

fn dns_records_from_slice(
    data: &ResourceRecord,
    len: Int<64>,
) -> List<DnsRecord> {
    let _ = specialize(len);
    if len == 0w64 {
        []
    } else {
        let rr = into_dns_record(*data[len - 1w64].data);
        let rest = dns_records_from_slice(data, len - 1w64);
        if rr.rtype == DnsRRType.OPT {
            // Omit OPT RRs
            rest
        } else {
            [rr] ++ rest
        }
    }
}

use %NS.0 as struct Ns {
    header: RRHeader,
    ns: String,
}

// Map a coredns `RR` into a DnsRecord.
// Operates on the fact that all `RR`s in coredns have a first field
// of type `RR_Header`, which holds the domain name and RRType as its
// first two fields.
fn into_dns_record(rr: &Int<8>) -> DnsRecord {
    let header = *(rr as &RRHeader);
    let name = header.name;
    let rrtype = header.rrtype;
    let _ = specialize(rrtype);
    
    let rname = into_dns_name(name.data, name.len); // there should only be one here
    let rtype = into_dns_rrtype(rrtype);
    let rdata = if rtype == DnsRRType.NS {
        let ns = *(rr as &Ns).ns;
        into_dns_name(ns.data, ns.len)
    } else {
        []
    };

    DnsRecord {
        rname: rname,
        rtype: rtype,
        rdata: rdata,
    }
} 

fn into_dns_rrtype(rrtype: Int<16>) -> DnsRRType {
    if rrtype == 1w16 { DnsRRType.A } else {
    if rrtype == 2w16 { DnsRRType.NS } else {
    if rrtype == 5w16 { DnsRRType.CNAME } else {
    if rrtype == 6w16 { DnsRRType.SOA } else {
    if rrtype == 15w16 { DnsRRType.MX } else {
    if rrtype == 16w16 { DnsRRType.TXT } else {
    if rrtype == 28w16 { DnsRRType.AAAA } else {
    if rrtype == 39w16 { DnsRRType.DNAME } else {
    if rrtype == 41w16 { DnsRRType.OPT } else {
    if rrtype == 251w16 || rrtype == 252w16 { DnsRRType.XFR } else {
    // if rrtype == 33w16 { DnsRRType.SRV } else {
    if rrtype == 43w16 { DnsRRType.DS } else {
    // if rrtype == 46w16 { DnsRRType.RRSIG } else {
    // if rrtype == 47w16 { DnsRRType.NSEC } else {
        DnsRRType.OTHER
    }}}}}}}}}}}
} 

// Map a coredns domain name into the form of `List<Int<8>>`, which
// is the standard form used in the reference model.
fn into_dns_name(data: &Int<8>, len: Int<64>) -> List<Int<8>> {
    let _ = specialize(len);
    if len == 0w64 {
        []
    } else {
        into_dns_name(
            data,
            len - 1w64,
        ) ++ [*data[len - 1w64]]
    }
}

// ——————————
// Reference Model
// ——————————

enum DnsRRType {
    EMPTY,
    SOA,
    NS,
    A,
    AAAA,
    CNAME,
    DNAME,
    TXT,
    MX,
    RRSIG,
    DS,
    SRV,
    NSEC,
    OPT,
    XFR, // AXFR and IXFR
    OTHER,
}

enum DnsRCode {
    NOERROR,
    NXDOMAIN,
    OTHER,
}

// The wild card ASCII code
fn wild_card_code() -> Int<8> { 42w8 }

// The dot ASCII code
fn dot_code() -> Int<8> { 46w8 }

struct DnsQuery {
    qname: List<Int<8>>,
    qtype: DnsRRType, 
}

struct DnsRecord {
    rname: List<Int<8>>,
    rtype: DnsRRType, 
    rdata: List<Int<8>>,
}

struct DnsZone {
    zone_name: List<Int<8>>,
    rrs: List<DnsRecord>, 
}

struct DnsResponse {
    rcode: DnsRCode, 
    flag_aa: Bool, 
    answer: List<DnsRecord>,
    authority: List<DnsRecord>,
    additional: List<DnsRecord>,
}

fn is_parent (rname: List<Int<8>>, qname: List<Int<8>>) -> Bool {
    let rlen = len(rname);
    let qlen = len(qname);
    rlen <=s qlen                                                // `qname` is not shorter
    && list_eq::<Int<8>>(rname, qname[qlen-rlen..])                       // `rname` is a suffix of `qname`
    && (qlen == rlen || qname[qlen-rlen-1] == dot_code())       // `qname` has a dot right before that
}

fn is_wild_card_domain (rr: DnsRecord) -> Bool {
    let rname = rr.rname;
    rname[0] == wild_card_code() 
    && rname[1] == dot_code()               // `rname` starts with "*."
    && rr.rtype != DnsRRType.EMPTY          // `rr` is not an empty non-terminal
}

fn is_wild_card_match(rr: DnsRecord, qname: List<Int<8>>) -> Bool {
    let rname = rr.rname;
    let rlen = len(rname);
    let qlen = len(qname);
    rlen <=s qlen                                               // `qname` is not shorter
    && is_wild_card_domain(rr)                                  // `rr` is wildcard
    && list_eq::<Int<8>>(rname[1..], qname[qlen-rlen+1..])         // `rname`, barring the "*", is a suffix of `qname`
    && (qname[qlen-rlen] != wild_card_code() 
    || qlen >s rlen && qname[qlen-rlen-1] != dot_code())        // `qname` does not also have exactly a "*" label at the position of the wildcard  
}

fn is_relevant_domain(rr: DnsRecord, qname: List<Int<8>>) -> Bool {
    let rname = rr.rname;
    if is_wild_card_domain(rr) {
        list_eq::<Int<8>>(rname, qname)
        || is_wild_card_match(rr, qname)        // `qname` is wildcard match
    } else {
        is_parent(rname, qname)                 // `qname` is a subdomain
    }
}

fn is_ns_match_record(rr: DnsRecord, qname: List<Int<8>>, zone_name: List<Int<8>>) -> Bool {
    rr.rtype == DnsRRType.NS                        // `rr` is NS
    && !list_eq::<Int<8>>(rr.rname, zone_name)      // `rr` is not the origin name
    // && is_relevant_domain(rr, qname)             // `qname` is relevant for `rr`
}

struct DnsRecordMatch {
    record: DnsRecord,
    len: Int,
}
fn filter_max_matches(rrs: List<DnsRecord>, qname: List<Int<8>>) -> List<DnsRecord> {
    let matches = map::<DnsRecord, DnsRecordMatch>(
        rrs, 
        |rr| {
            let rname = rev::<Int<8>>(rr.rname);
            let qname = rev::<Int<8>>(qname);
            DnsRecordMatch {
                record: rr,
                len: list_cmp::<Int<8>>(rname, qname),
            }
        }
    );
    let max_match = max::<DnsRecordMatch>(matches, |match| {match.len});
    map::<DnsRecordMatch, DnsRecord>(
        filter::<DnsRecordMatch>(matches, |match| { match.len == max_match }),
        |match| {match.record}
    )
}

fn get_relevant_rrs(
    query: DnsQuery,
    zone_name: List<Int<8>>,
    rrs: List<DnsRecord>
) -> List<DnsRecord> {
    let relevant_rrs = filter::<DnsRecord>(rrs, |rr| {is_relevant_domain(rr, query.qname)} );
    if len(relevant_rrs) == 0 { 
        // No relevant records found
        []
    } else {
        let ns_match_rrs = filter::<DnsRecord>(relevant_rrs, |rr| {is_ns_match_record(rr, query.qname, zone_name)} );
        if len(ns_match_rrs) == 0 {
            let max_match_rrs = filter_max_matches(relevant_rrs, query.qname);
            let wildcard_match_rrs = filter::<DnsRecord>(max_match_rrs, |rr| {is_wild_card_match(rr, query.qname)} );
            if len(wildcard_match_rrs) == 0 {
                // return all max matched records
                max_match_rrs
            } else {
                wildcard_match_rrs
            }
        } else {
            // First matches NS records
            ns_match_rrs
        }
    }
}

// Get the glue records for NS results
fn delegation(ns_records: List<DnsRecord>, all_records: List<DnsRecord>) -> List<DnsRecord> {
    let parsing_records = filter::<DnsRecord>(all_records, |x| {(x.rtype == DnsRRType.A) || (x.rtype == DnsRRType.AAAA)} );
    let glue_records = filter::<DnsRecord>(
        parsing_records, 
        |rr| {
            any::<DnsRecord>(
                ns_records, 
                |ns_rr| { list_eq::<Int<8>>(ns_rr.rdata, rr.rname) } 
            )
        }
    );
    glue_records
}

fn exact_match(
    relevant_rrs: List<DnsRecord>,
    query: DnsQuery,
    zone: DnsZone,
) -> DnsResponse {
    let ns_records = filter::<DnsRecord>(relevant_rrs, |x| {x.rtype == DnsRRType.NS} );
    if all::<DnsRecord>(relevant_rrs, |x| {x.rtype != DnsRRType.SOA}) 
        && len(ns_records) != 0 
    {
        let glue_records = delegation(ns_records, zone.rrs);
        DnsResponse {
            rcode: DnsRCode.NOERROR, 
            flag_aa: false,
            answer: [], 
            additional: glue_records, 
            authority: ns_records,
        }
    } else {
        let ans_records = filter::<DnsRecord>(relevant_rrs, |x| {x.rtype == query.qtype} );
        if len(ans_records) != 0 {
            if query.qtype == DnsRRType.NS {
                // NS record triggers additional handling
                let delegated = delegation(ans_records, zone.rrs);
                DnsResponse {
                    rcode: DnsRCode.NOERROR, 
                    flag_aa: true,
                    answer: ans_records, 
                    additional: delegated, 
                    authority: [], 
                }
            } else {
                // CoreDNS will return the apex NS records here
                let apex_ns = filter::<DnsRecord>(zone.rrs, |rr| { 
                    rr.rtype == DnsRRType.NS
                    && list_eq::<Int<8>>(rr.rname, zone.zone_name)
                });
                DnsResponse {
                    rcode: DnsRCode.NOERROR, 
                    flag_aa: true,
                    answer: ans_records, 
                    additional: [], 
                    authority: apex_ns,
                }
            }
        } else {
            let cname_rrs = filter::<DnsRecord>(relevant_rrs, |x| {x.rtype == DnsRRType.CNAME} );
            if len(cname_rrs) != 0 {
                DnsResponse { 
                    rcode: DnsRCode.NOERROR, 
                    flag_aa: true,
                    answer: cname_rrs, 
                    additional: [], 
                    authority: [], 
                }
            } else {
                let soa_records = filter::<DnsRecord>(zone.rrs, |x| {x.rtype == DnsRRType.SOA} );
                DnsResponse {
                    rcode: DnsRCode.NOERROR, 
                    flag_aa: true,
                    answer: [], 
                    additional: [], 
                    authority: soa_records, 
                }
            }
        }
    }
}

fn rrlookup(zone: DnsZone, query: DnsQuery) -> DnsResponse {
    let relevant_rrs = get_relevant_rrs(query, zone.zone_name, zone.rrs);
    if len(relevant_rrs) == 0 {
        let soa_records = filter::<DnsRecord>(zone.rrs, |x| {x.rtype == DnsRRType.SOA} );
        DnsResponse { 
            rcode: DnsRCode.NXDOMAIN, 
            flag_aa: true,
            answer: [], 
            additional: [], 
            authority: soa_records, 
        }
    } else {
        if any::<DnsRecord>(relevant_rrs, |x| {list_eq::<Int<8>>(x.rname, query.qname)}) {
            exact_match(relevant_rrs, query, zone)
        } else {
            if any::<DnsRecord>(relevant_rrs, |rr| {is_wild_card_match(rr, query.qname)}) {
                exact_match(relevant_rrs, query, zone) // HACK: the wildcard name is NOT rewritten
            } else {
                let ns_rrs = filter::<DnsRecord>(relevant_rrs, |x| {x.rtype == DnsRRType.NS} );
                let has_soa = any::<DnsRecord>(relevant_rrs, |x| {x.rtype == DnsRRType.SOA} );
                if len(ns_rrs) != 0 && !has_soa {
                    let glue_records = delegation(ns_rrs, zone.rrs);
                    DnsResponse { 
                        rcode: DnsRCode.NOERROR, 
                        flag_aa: false,
                        answer: [], 
                        additional: glue_records, 
                        authority: ns_rrs, 
                    }
                } else {
                    let soa_records = filter::<DnsRecord>(zone.rrs, |x| {x.rtype == DnsRRType.SOA} );
                    DnsResponse {
                        rcode: DnsRCode.NXDOMAIN, 
                        flag_aa: true,
                        answer: [],
                        additional: [], 
                        authority: soa_records, 
                    }
                }
            }
        }
    }
}
