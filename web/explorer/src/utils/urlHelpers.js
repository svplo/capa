/**
 * Creates an MBC (Malware Behavior Catalog) URL from an MBC object.
 *
 * @param {Object} mbc - The MBC object to format.
 * @param {string} mbc.id - The ID of the MBC entry.
 * @param {string} mbc.objective - The objective of the malware behavior.
 * @param {string} mbc.behavior - The specific behavior of the malware.
 * @returns {string|null} The MBC URL or null if the ID is invalid.
 */
export function createMBCHref(mbc) {
    let baseUrl;

    // Determine the base URL based on the id
    if (mbc.id.startsWith("B")) {
        // Behavior
        baseUrl = "https://github.com/MBCProject/mbc-markdown/blob/main";
    } else if (mbc.id.startsWith("C")) {
        // Micro-Behavior
        baseUrl = "https://github.com/MBCProject/mbc-markdown/blob/main/micro-behaviors";
    } else {
        return null;
    }

    // Convert the objective and behavior to lowercase and replace spaces with hyphens
    const objectivePath = mbc.objective.toLowerCase().replace(/\s+/g, "-");
    const behaviorPath = mbc.behavior.toLowerCase().replace(/\s+/g, "-");

    // Construct the final URL
    return `${baseUrl}/${objectivePath}/${behaviorPath}.md`;
}

/**
 * Creates a MITRE ATT&CK URL for a specific technique or sub-technique.
 *
 * @param {Object} attack - The ATT&CK object containing information about the technique.
 * @param {string} attack.id - The ID of the ATT&CK technique or sub-technique.
 * @returns {string|null} The formatted MITRE ATT&CK URL for the technique or null if the ID is invalid.
 */
export function createATTACKHref(attack) {
    const baseUrl = "https://attack.mitre.org/techniques/";
    const idParts = attack.id.split(".");

    if (idParts.length === 1) {
        // It's a technique
        return `${baseUrl}${idParts[0]}`;
    } else if (idParts.length === 2) {
        // It's a sub-technique
        return `${baseUrl}${idParts[0]}/${idParts[1]}`;
    } else {
        return null;
    }
}
